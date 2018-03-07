import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import leastsq
import peakutils
import pyodbc 
import matplotlib.pyplot as plt

columnNameList = ['startDayHour','externalServiceName','externalServiceCall','requestUrl','numSamples','maxDuration','duration_P50','duration_P75','duration_P95','duration_P99']
densityLength = 1000

def connectDB():
    server = 'tcp:ucmloggingdatawarehouse.database.windows.net,1433' 
    database = 'ucmloggingdatawarehouse' 
    username = 'loggingDW_readonly' 
    password = 'Read@Only123' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def getSQLQuery(externalServiceName, requestUrl):
    columnNames = ""
    for name in columnNameList:
        columnNames = columnNames + "[" + name + "],"
    columnNames = columnNames[0:len(columnNames)-1]
    sqlQuery = "SELECT " + columnNames + \
            "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
            "where externalServiceName = '" + externalServiceName +"' and " + \
            "requestUrl='" + requestUrl + "' and " + \
            "externalServiceCall='All' and " + \
            "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday'" + \
            "order by startDayHour"
    return sqlQuery

def loadData(cursor, externalServiceName, requestUrl):
    sqlQuery = getSQLQuery(externalServiceName, requestUrl)
    cursor.execute(sqlQuery)
    df = pd.DataFrame()
    row = cursor.fetchone()
    while row:
        rowAsList = [d for d in row]
        dfRow = pd.DataFrame([rowAsList])
        df = df.append(dfRow)
        row = cursor.fetchone()
    df = df.rename(columns=lambda x: columnNameList[x])
    return df

def gaussFunc(par, t):
    return (par[0]/par[1])*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2)))

def errFunc(par, t, y):
    err= y - gaussFunc(par,t)
    return err

def getDensity(origin):
    xmin = origin.min()
    xmax = origin.max()
    xs = np.linspace(xmin*0.5,xmax*1.2,densityLength)
    densityFunc= stats.gaussian_kde(origin)
    ys = densityFunc(xs)
    density = {"x":xs,"y":ys}
    return density

def getP0(density):
    xs = density['x']
    ys = density['y']
    indices= peakutils.indexes(-ys)
    indices= np.append(indices,0)
    indices= np.append(indices,densityLength-1)
    peakIndex= np.argmax(ys)
    peakMax= xs[peakIndex]
    valleyDis= abs(indices-peakIndex)
    valleyNear= xs[indices[np.argmin(valleyDis)]]
    muEst = peakMax
    sEst = abs(peakMax-valleyNear)/2
    p0 = [1/np.sqrt(2*np.pi)/sEst, sEst, muEst]
    return p0

def saveChart(density,origin,anomaly):
    fig= plt.figure(figsize = (20, 7))
    plt.subplot(1,2,1)
    plt.plot(density['x'],density['y'])
    plt.plot(density['x'],density['yEst'])
    plt.subplot(1,2,2)
    plt.plot(origin.startDayHour, origin.duration_P75)
    plt.plot(anomaly.startDayHour, anomaly.duration_P75,'ro')
    fig.savefig('{}.png'.format(origin.iloc[-1].startDayHour))
    plt.close(fig)

def getThreshold(pEst):
    mu= pEst[0][2]
    s= pEst[0][1]
    return mu+2*s

cursor = connectDB()
data = loadData(cursor,'CampaignAggregatorService','https://api.ucm.bingads.microsoft.com/api/v2/DataTable/BobAccounts')
period = 120
endIndex = len(data)
for i in range(period,endIndex):
    t0= i-period
    origin = data[t0:i]
    perf = origin.duration_P75
    density = getDensity(perf)
    p0 = getP0(density)
    pEst= leastsq(errFunc, p0, args = (density['x'], density['y']))
    density['yEst'] = gaussFunc(pEst[0],density['x'])
    threshold = getThreshold(pEst)
    anomaly = origin[perf>threshold]    
    if (anomaly.iloc[-1].startDayHour == origin.iloc[-1].startDayHour):
        saveChart(density, origin, anomaly)
        #createIcM
 