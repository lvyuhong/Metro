
import pandas as pd
import numpy as np

def MeanMethod(test1,ret_list):
    for f in ret_list:
        print('------------开始计算:',f,'----------------')
        df1=pd.read_csv(path+f)
        df1['hour'] = df1['time'].apply(lambda x : x[11:15]+'0')

        df = pd.DataFrame()
        g = df1.groupby(['hour','stationID'])
        df['inCount'] = g['status'].sum()
        df['outCount'] = g['status'].count()-df['inCount']
        df.reset_index(drop=False,inplace=True)
    
        test1 = test1.merge(df,on=['hour','stationID'],how='left')
        test1 = test1.fillna(0)
        test1['inNums'] = test1['inNums']+test1['inCount']
        test1['outNums'] = test1['inNums']+test1['outCount']
        test1 = test1[['stationID','startTime','endTime','inNums','outNums','hour']]
    return test1

## k=15 10min粒度，k=
def genLinesSeries(path,fileList,timetype):
    lines = pd.DataFrame()
    for f in fileList:
        print('------------开始计算:',f,'----------------')
        ## 读取数据
        df=pd.read_csv(path+f)
        if timetype=='mins':
            df['time'] = df['time'].apply(lambda x : x[:15]+'0')
        elif timetype=='hour':
            df['time'] = df['time'].apply(lambda x : x[:13])
        elif timetype=='day':
            df['time'] = df['time'].apply(lambda x : x[:10])

        ## out
        df0 = pd.DataFrame()
        g = df[df['status']==0].groupby(['time','lineID'])
        df0 = g.agg({'status':'count','deviceID':'nunique','userID':'nunique'})
        df0.columns = ['outCount','outDevices','outUsers']
        df0.reset_index(drop=False,inplace=True)

        ## in
        df1 = pd.DataFrame()
        g = df[df['status']==1].groupby(['time','lineID'])
        df1 = g.agg({'status':'count','deviceID':'nunique','userID':'nunique'})
        df1.columns = ['inCount','inDevices','inUsers']
        df1.reset_index(drop=False,inplace=True)
    
        day = df0.merge(df1,on=['time','lineID'])
        lines = pd.concat([lines,day],axis=0)
    return lines
    
def genStationSeries(path,fileList,timetype):
    days = pd.DataFrame()
    for f in fileList:
        print('------------开始计算:',f,'----------------')
        ## 读取数据
        df=pd.read_csv(path+f)
        if timetype=='mins':
            df['time'] = df['time'].apply(lambda x : x[:15]+'0')
        elif timetype=='hour':
            df['time'] = df['time'].apply(lambda x : x[:13])
        elif timetype=='day':
            df['time'] = df['time'].apply(lambda x : x[:10])

        ## out
        df0 = pd.DataFrame()
        g = df[df['status']==0].groupby(['time','lineID','stationID'])
        df0 = g.agg({'status':'count','deviceID':'nunique','userID':'nunique'})
        df0.columns = ['outCount','outDevices','outUsers']
        df0.reset_index(drop=False,inplace=True)

        ## in
        df1 = pd.DataFrame()
        g = df[df['status']==1].groupby(['time','lineID','stationID'])
        df1 = g.agg({'status':'count','deviceID':'nunique','userID':'nunique'})
        df1.columns = ['inCount','inDevices','inUsers']
        df1.reset_index(drop=False,inplace=True)
    
        day = df0.merge(df1,on=['time','lineID','stationID'])
        days = pd.concat([days,day],axis=0)
    return days