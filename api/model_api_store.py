from flask import Flask,request
import joblib as jb
import pandas as pd
from lojas.Store_v2 import Store

# Inicializando o Flask
app = Flask(__name__)

 
# Carregando o modelo
md = jb.load('/home/antoniojunior/Documentos/forecast_stores/model/md.pkl')


@app.route('/Store/predtic',methods=['POST'])
def store_predtic():
    Dados_api = request.get_json() #Dados de entrada do API
    

# Coletando os dados e enviando para o API
    if Dados_api:
        if isinstance(Dados_api,dict): # Quando a entrada for apenas uma linha
            df_raw = pd.DataFrame(Dados_api,index=[0])
        else : #Quando os dados forem diversas linhas
            df_raw = pd.DataFrame(Dados_api,columns =Dados_api[0].keys())
            
# Tratamento dos dados
    pipeline = Store()
 
    df = pipeline.union_df(df_raw)
    df = pipeline.total_dias(df)
    df = pipeline.reneming_columns(df)
    df = pipeline.Treatment_time_variables(df)
    df = pipeline.Treatment_obj_variables(df)
    df = pipeline.creat_variables(df)
    df = pipeline.Eliminated_stores(df)
    df = pipeline.deleted_columns(df)
    df = pipeline.dummies_var(df)
    df = pipeline.order_df(df)
    df = pipeline.transformed_time_variables(df)
    df = pipeline.Treatment_assortment_holiday(df)
    df = pipeline.format_df(df)
    
    X = df.drop(columns = ['date','total_dias'])


# Predições 
    pred = md.predict(X)
    
    
# Retornando a predição para o cliente
    df['Pred'] = pred

    return df.to_json(orient = 'records')



if __name__=='__main__':
    # start api
    app.run(host='0.0.0.0',port='5000')
   