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

usecols=['season','holiday','workingday','weather','temp','atemp','humidity','windspeed','count']
df=pd.read_csv('train.csv',usecols=usecols)
###
#StandardScaler
###
nonstand=df[['season','holiday','workingday','weather']]
stand=df[['temp','atemp','humidity','windspeed']]
train_label=df['count']

scaler=StandardScaler()
scaler.fit(stand)
scaled_features = scaler.transform(stand)
df_feat = pd.DataFrame(scaled_features,columns=['temp','atemp','humidity','windspeed'])
df_feat['season']=nonstand['season']
df_feat['holiday']=nonstand['holiday']
df_feat['workingday']=nonstand['workingday']
#print(df_feat.head())
train_data=df_feat
###
if prediction_evaluation_switch==1:
    X_train,X_test,Y_train,Y_test=train_test_split(train_data, train_label, test_size=0.2)
    knn=KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train,Y_train)
    pre=knn.predict(X_test)
    print('pre   actual')
    count=0
    for a in Y_test:
        print(pre[count],' ',end='')
        print(a)
        count+=1
        if count>=10:
            break
    # for i in range(10):
    #     print(pre[i])
###
if prediction_evaluation_switch!=1:
    usecolstest=['season','holiday','workingday','weather','temp','atemp','humidity','windspeed']
    dftest=pd.read_csv('test.csv',usecols=usecolstest)
    nonstandtest=dftest[['season','holiday','workingday','weather']]
    standtest=dftest[['temp','atemp','humidity','windspeed']]
    scalert=StandardScaler()
    scaler.fit(standtest)
    scaled_featurestest = scaler.transform(standtest)
    df_feattest = pd.DataFrame(scaled_featurestest,columns=['temp','atemp','humidity','windspeed'])
    df_feattest['season']=nonstandtest['season']
    df_feattest['holiday']=nonstandtest['holiday']
    df_feattest['workingday']=nonstandtest['workingday']
    test_data=df_feattest
    knn=KNeighborsRegressor(n_neighbors=5)
    knn.fit(train_data,train_label)
    pre=knn.predict(test_data)
    for i in range(len(pre)):
        pre[i]=round(pre[i])
    '''
    output csv
    '''
    df_date_time=open('test.csv',mode='r',newline='')
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


# dftest=pd.read_csv('test.csv',index_col=0,usecols=usecols)
# mse=[]
# most=None
# most_num=1
# for k in range(1,100):
#     knn=KNeighborsRegressor(n_neighbors=k)
#     knn.fit(X_train,Y_train)
#     prd=knn.predict(X_test)
#     mse.append(metrics.mean_squared_error(prd,Y_test))
# k_range=range(1,100)
# plt.plot(k_range,mse)
# plt.show()
# for k in range(0,99):
#     if most<prd[k]:
#         most=prd[k]
#         most_num=k+1
# print(most)
# print(most_num)


# for i in range(len(pre)):
#     wri.write(df_date_time[i]['datetime'])
#     wri.write(',')
#     wri.write(pre[i])
#     wri.write('\n')
