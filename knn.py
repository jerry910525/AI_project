import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
from sklearn import datasets
import csv

prediction_evaluation_switch=1

usecols=['datetime','season','holiday','workingday','weather','temp','atemp','humidity','windspeed','count']
df=pd.read_csv('train.csv',usecols=usecols)
df['datetime']=pd.to_datetime(df['datetime'],format='%Y-%m-%d %H:%M:%S')
df['hour']=df['datetime'].dt.hour
###
#StandardScaler
###
nonstand_col=[]
stand_col=['hour','season','holiday','workingday','weather','temp','atemp','humidity','windspeed']
nonstand=df[nonstand_col]
stand=df[stand_col]
train_label=df['count']

scaler=StandardScaler()
scaler.fit(stand)
scaled_features = scaler.transform(stand)
df_feat = pd.DataFrame(scaled_features,columns=stand_col)
for i in nonstand_col:
    df_feat[i]=nonstand[i]
#print(df_feat.head())
train_data=df_feat
###
if prediction_evaluation_switch==1:
    X_train,X_test,Y_train,Y_test=train_test_split(train_data, train_label, test_size=0.2)
    least=None
    least_k=1
    R_plot=[]
    for k in range(1,100):
        knn=KNeighborsRegressor(n_neighbors=k)
        Y_train_log=Y_train.apply(np.log)
        knn.fit(X_train,Y_train_log)
        prd=knn.predict(X_test)
        prd=np.exp(prd)
        MSLE=metrics.mean_squared_log_error(prd,Y_test)
        RMSLE=MSLE**0.5
        R_plot.append(RMSLE)
        if least==None or least>RMSLE:
            least_k=k
            least=RMSLE
    k_range=range(1,100)
    plt.plot(k_range,R_plot)
    plt.xlabel('k value')
    plt.ylabel('RMSLE')
    plt.show()
    print('best K = ',least_k,' with RMSLE ',least)

###
if prediction_evaluation_switch==1:
    usecolstest=['datetime','season','holiday','workingday','weather','temp','atemp','humidity','windspeed']
    dftest=pd.read_csv('test_1.csv',usecols=usecolstest)
    dftest['datetime']=pd.to_datetime(dftest['datetime'],format='%Y-%m-%d %H:%M:%S')
    dftest['hour']=dftest['datetime'].dt.hour
    nonstandtest=dftest[nonstand_col]
    standtest=dftest[stand_col]
    scalert=StandardScaler()
    scaler.fit(standtest)
    scaled_featurestest = scaler.transform(standtest)
    df_feattest = pd.DataFrame(scaled_featurestest,columns=stand_col)
    for i in nonstand_col:
        df_feattest[i]=nonstandtest[i]
    test_data=df_feattest
    knn=KNeighborsRegressor(n_neighbors=least_k)
    knn.fit(train_data,train_label.apply(np.log))
    pre=knn.predict(test_data)
    for i in range(len(pre)):
        pre[i]=np.floor(np.exp(pre[i]))
    '''
    output csv
    '''
    df_date_time=open('test_1.csv',mode='r',newline='')
    rows=csv.DictReader(df_date_time)
    wri=open('bike_prediction.txt',mode='w',newline='')
    wri.write('datetime,count\n')
    count=0
    for row in rows:
        wri.write(row['datetime'])
        wri.write(',')
        wri.write(str(pre[count]))
        wri.write('\n')
        count+=1
    print('finish writing')

