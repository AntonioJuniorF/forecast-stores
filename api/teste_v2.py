
import pandas as pd
from lojas.Store_v2 import Store
from lojas.Store_v1 import Store1

from lightgbm import LGBMRegressor
import joblib as jb

d = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/test.csv',low_memory=False)

pipeline = Store()
 
df = pipeline.union_df(d)
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


#model = jb.load('/home/antoniojunior/Documentos/forecast_stores/model/md.pkl')

train = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/train.csv',low_memory=False)
store = pd.read_csv('/home/antoniojunior/Documentos/forecast_stores/dados/store.csv',low_memory=False)


pipeline = Store1()
 
df1 = pipeline.union_df(train,store)
df1 = pipeline.total_dias(df1)
df1 = pipeline.reneming_columns(df1)
df1 = pipeline.Treatment_time_variables(df1)
df1 = pipeline.Treatment_obj_variables(df1)
df1 = pipeline.creat_variables(df1)
df1 = pipeline.Eliminated_stores(df1)
df1 = pipeline.deleted_columns(df1)
df1 = pipeline.dummies_var(df1)
df1 = pipeline.order_df(df1)
df1 = pipeline.transformed_time_variables(df1)
df1 = pipeline.Treatment_assortment_holiday(df1)


X      = df1.copy()
X_test = df.copy()

X      = X.drop(columns = ['date','sales','total_dias'])
X_test = X_test.drop(columns = ['date','total_dias'])

Y = df1[['sales']]

# LGBM
lr = 0.07050672582272845
max_depth  = 9
n_estimators = 855
colsample_bytree = 1
lamb             = 0.00039939957529561544
alpha            =  0.0006803520566543689

model = LGBMRegressor(learning_rate=lr, num_leaves=2 ** max_depth, max_depth=max_depth, 
                         n_estimators=n_estimators, random_state=40, n_jobs=6)

md       = model.fit(X,Y)
y_pred  = md.predict(X_test)

md       = model.fit(X,Y)

jb.dump(md, "md.pkl")



md1 = jb.load('md.pkl')

y_pred3  = md.predict(X_test)
