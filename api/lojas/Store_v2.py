import numpy as np
import pandas as pd 
import inflection
import math
import datetime

class Store:
    
    def __init__(self):
        
        self.train = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/train.csv',low_memory=False)
        self.store = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/store.csv',low_memory=False)
        self.lojas = np.load('/home/antoniojunior/Documentos/forecast_stores/model/lojas_delet.npy')


    def union_df(self,dados):
        dados = dados.drop(columns = 'Unnamed: 0')
        t = pd.concat((self.train,dados))
        df = pd.merge(t, self.store, how="left", on="Store")
        # convert variable to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df
    
    def total_dias(self,df):
        dias_mes = []
        for i in range(1,13):
            dias_mes.append(np.max(df['Date'].dt.day[df['Date'].dt.month == i]))

        soma_dias = []

        for i in range(1,13):
            soma_dias.append(np.sum(dias_mes[:i]))

        vetor = np.zeros(df.shape[0])

        for i in range(2,13):
            vetor[df['Date'].dt.month == i] = soma_dias[i -2]

        df['Total_dias']= vetor + df['Date'].dt.day 
        df['Total_dias'][df['Date'].dt.year == 2014] = df['Total_dias'][df['Date'].dt.year == 2014] + df['Total_dias'][df['Date'].dt.year == 2013].unique()[0]
        df['Total_dias'][df['Date'].dt.year == 2015] = df['Total_dias'][df['Date'].dt.year == 2015] + df['Total_dias'][df['Date'].dt.year == 2014].unique()[0]
        
        return df
    
    def reneming_columns(self,df):
        Colunas_nova = df.columns.tolist()
        snakecase    = lambda x: inflection.underscore(x)
        cols_new     = list(map(snakecase, Colunas_nova))
        df.columns   = cols_new

        return df
    
    def Treatment_time_variables(self,df):
        Copetion_nan_store = df['store'][df['competition_open_since_year'].isna()] # lojas que não tem comcorrentes
        Copetion_store  = df['store'][df['competition_open_since_year'].isna() ==False ] # lojas que tem concorrentes

        df.competition_open_since_year = df.apply(lambda x: x["date"].year if math.isnan(x["competition_open_since_year"]) else x["competition_open_since_year"], axis=1)
        df.competition_open_since_month = df.apply(lambda x: x["date"].month if math.isnan(x["competition_open_since_month"]) else x["competition_open_since_month"], axis=1)

        df["competition_open_since_year"]  = np.int64(df["competition_open_since_year"])
        df["competition_open_since_month"] = np.int64(df["competition_open_since_month"])

        vetor = np.zeros(df.shape[0])
        vetor[Copetion_store.index] = 1
        df['without_competition'] = vetor # marcando se a loja tem concorrente ou não.

        df["promo2_since_year"] = df.apply(lambda x: x["date"].year if math.isnan(x["promo2_since_year"]) else x["promo2_since_year"], axis=1)
        df["promo2_since_week"] = df.apply(lambda x: x["date"].week if math.isnan(x["promo2_since_week"]) else x["promo2_since_week"], axis=1)

        df["promo2_since_year"] = np.int64(df["promo2_since_year"])
        df["promo2_since_week"] = np.int64(df["promo2_since_week"])

        month_map = {1: "Jan", 2: "Fev", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        df["month_map"] = df["date"].dt.month.map(month_map)
        df["promo_interval"].fillna('a', inplace=True)
        df["is_promo"] = df[["promo_interval", "month_map"]].apply(lambda x: 0 if x["promo_interval"] == 0 else 1 if x["month_map"] in x["promo_interval"].split(",") else 0, axis=1)        
        df = df.drop(columns = ['promo_interval','month_map'])
        df["competition_distance"] = df["competition_distance"].fillna(200000)

        return df



    def Treatment_obj_variables(self,df):
        ind                            = df.columns[df.dtypes == 'object'] # variáveis string
        df.loc[df[ind[0]] == 0,ind[0]] = '0'

        df["assortment"]    = df["assortment"].apply(lambda x: "basic" if x == "a" else "extra" if x == "b" else "extended")
        df["state_holiday"] = df["state_holiday"].apply(lambda x: "public_holiday" if x == "a" else "easter_holiday" if x == "b" else "christmas" if x == "c" else "regular_day")
        return df 
  
    def creat_variables(self,df):
        df["year"]       = df["date"].dt.year  # ano
        df["month"]      = df["date"].dt.month # mês
        df["day"]        = df["date"].dt.day   # dia
        df['week_year']  = df["date"].dt.week # Semana do ano
  

        df["competition_since"] = df.apply(lambda x: datetime.datetime(year=x["competition_open_since_year"], month=x["competition_open_since_month"], day=1), axis=1)

        df["competition_time_month"] = ((df["date"] - df["competition_since"]) / 30)
        df['competition_time_month'] = df["competition_time_month"].dt.days

        df["promo_since"]     = df["promo2_since_year"].astype(str) + "-" + df["promo2_since_week"].astype(str)
        df["promo_since"]     = df["promo_since"].apply(lambda x: datetime.datetime.strptime(x + "-1", "%Y-%W-%w") - datetime.timedelta(days=7))
        df["promo_time_week"] = ((df["date"] - df["promo_since"]) / 7)
        df["promo_time_week"] = df["promo_time_week"].dt.days

        df['week_year']   =  np.int64(df['week_year']) 
        df['day']         =  np.int64(df['day'])
        df['month']       =  np.int64(df['month'])  
        df['year']        =  np.int64(df['year']) 

        return df 
    
    def Eliminated_stores(self,df):
  
        for i in range(len(self.lojas)):
            
            df = df[df['sales'] > 0]
            df = df[df['date'] >'2013-01-02']
            df.index = np.arange(df.shape[0])
            df = df.drop(df[df['store'] == self.lojas[i]].index.values)

        return df

    
    def deleted_columns(self,df):
        col = ['competition_since','promo_since','open','month','competition_time_month',
               'school_holiday','competition_open_since_month','promo2_since_week',
               'is_promo']
        df = df.drop(columns = col)
        return df
    
    def dummies_var(self,df):
        coluna =['state_holiday','store_type','assortment']
        df = df.join(pd.get_dummies(df[coluna], prefix=coluna))
        df = df.drop(columns=coluna)
        return df 
    
    def order_df(self,df):
        df = df.reindex(index=df.index[::-1])
        df.index = np.arange(df.shape[0])
        return df
    
    def transformed_time_variables(self,df):
        df['day_cos'] = df['day'].apply(lambda x: np.cos(x * (2. * np.pi/30)))
        df = df.drop(columns = 'day')
        return  df


    def Treatment_assortment_holiday(self,df):
        cold = ['assortment_extended','assortment_extra',
                'assortment_basic']

        vetor = np.zeros(df.shape[0])
        vetor[df['assortment_extended'] == 1] = 1
        vetor[df['assortment_extra'] == 1] = 2
        vetor[df['assortment_basic'] == 1] = 0
        df['assortment'] = vetor

        df = df.drop(columns = cold)
  
        vetor = np.zeros(df.shape[0])

        vetor[df['state_holiday_christmas'] == 1] = 1
        vetor[df['state_holiday_easter_holiday'] == 1] = 1
        vetor[df['state_holiday_public_holiday'] == 1] = 1
        vetor[df['state_holiday_regular_day'] == 1] = 0
  
        df['holiday'] = vetor

        cold = ['state_holiday_regular_day','state_holiday_public_holiday',
                'state_holiday_easter_holiday','state_holiday_christmas','store_type_d']

        df = df.drop(columns = cold)

        return df
    
    def format_df(self,df):

        df.index = np.arange(df.shape[0])
        df = df.drop(columns = ['id','sales'])

        return df