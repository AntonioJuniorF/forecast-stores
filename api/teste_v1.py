import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_log_error,mean_squared_error
from lightgbm import LGBMRegressor 
from lojas.Store_v1 import Store


train = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/train.csv',low_memory=False)
store = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/store.csv',low_memory=False)


pipeline = Store()
 
df = pipeline.union_df(train,store)
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

def dados_teste_val(df):
  val   = df.copy()
  test  = df.copy()
  
  val  = val[val['date'] < '2015-06-19']     # Dados de validação
  test = test[test['date'] >= '2015-06-19']  # Dados de teste
  Date = val['date']
  df.index = np.arange(df.shape[0])
  X = val.drop(columns = ['date','sales'])
  Y = val[['sales','total_dias']]

  return X,Y,Date  

X,Y,Date = dados_teste_val(df)  

lr = 0.07050672582272845
max_depth  = 9
n_estimators = 855
colsample_bytree = 1
lamb             = 0.00039939957529561544
alpha            =  0.0006803520566543689

model = LGBMRegressor(learning_rate=lr, num_leaves=2 ** max_depth, max_depth=max_depth, 
                         n_estimators=n_estimators, random_state=40, 
                         n_jobs=6)


def MAPE(y_pred,Y_teste):
  return np.mean(100*np.abs(y_pred - Y_teste)/np.abs(Y_teste))


def validation1(X,Y,coluna,flag,Date,model):
  vetor_MAPE = np.zeros(5) 
  vetor_MSLR = np.zeros(5)
  vetor_RMSE = np.zeros(5)
  for i in range(5):
    # Dados de treinamento
    print('Data do inicio do treinamento:', Date[X['total_dias'] < 689 + 6*7*i].dt.date.values[0],
          'Data do final do treinamento :',Date[X['total_dias'] < 689 + 6*7*i].dt.date.values[-1])
  
    
    X_t = X[X['total_dias']  < 689 + 6*7*i]
    y_t = Y[coluna][Y['total_dias']  < 689 + 6*7*i]
    X_t = X_t.drop(columns = ['total_dias'])
    
    # Dados de validação
    print('Data do inicio do Validação  :', Date[(X['total_dias'] >= 689 + 6*7*i) & (X['total_dias'] <= 689 + 6*7*(i+1))].dt.date.values[0],
          'Data do final do Validação   :',Date[(X['total_dias'] >= 689 + 6*7*i) & (X['total_dias'] <= 689 + 6*7*(i+1))].dt.date.values[-1])

    X_v = X[(X['total_dias'] >= 689 + 6*7*i) & (X['total_dias'] <= 689 + 6*7*(i+1))]
    y_v = Y[coluna][(Y['total_dias'] >= 689 + 6*7*i) & (Y['total_dias'] <= 689 + 6*7*(i+1))]
    X_v = X_v.drop(columns = ['total_dias'])
    
    md        = model.fit(X_t, y_t)
    y_pred    = md.predict(X_v)
    
    if flag == 'log':
      y_pred = np.round(10**y_pred - 1)  # eliminar o ruído provocado pelo computados atravez dou round
      y_v    = np.round(10**y_v - 1)
    if flag == 'sqrt':
      y_pred = np.round(y_pred**2)
      y_v    = np.round(y_v**2)
    if flag == 'normal':
      y_pred = y_pred
      y_v    = y_v
    
  
    
    mape = MAPE(y_v,y_pred)
    mslr = mean_squared_log_error(y_v,y_pred)
    rmse = mean_squared_error(y_v,y_pred,squared =False)
    vetor_MAPE[i] = mape
    vetor_MSLR[i] = mslr
    vetor_RMSE[i] = rmse
  
    print('MAPE: ',np.format_float_positional(mape,5))
    print('RMSLE:',np.format_float_positional(mslr,5))
    print('RMSE: ',np.format_float_positional(rmse,5))
     
   
  print('Mape Geral: ',np.format_float_positional(np.mean(vetor_MAPE),5),'Std:',np.format_float_positional(np.std(vetor_MAPE),5),'Erro:',np.format_float_positional(np.std(vetor_MAPE)/np.sqrt(5),5))
  print('Rmsle Geral:',np.format_float_positional(np.mean(vetor_MSLR),5),'Std:',np.format_float_positional(np.std(vetor_MSLR),5),'Erro:',np.format_float_positional(np.std(vetor_MSLR)/np.sqrt(5),5))
  print('Rmse Geral: ',np.format_float_positional(np.mean(vetor_RMSE),5),'Std:',np.format_float_positional(np.std(vetor_RMSE),5),'Erro:',np.format_float_positional(np.std(vetor_RMSE)/np.sqrt(5),5))
  return vetor_MAPE,vetor_MSLR,vetor_RMSE


vetor_MAPE3,vetor_MSLR3,vetor_RMSE3  = validation1(X,Y,'sales','normal',Date,model)

