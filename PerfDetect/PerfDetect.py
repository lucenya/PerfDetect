import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import leastsq
import peakutils
import pyodbc 
import matplotlib.pyplot as plt

columnNameList = ['startDayHour','externalServiceName','externalServiceCall','requestUrl','numSamples','maxDuration','duration_P50','duration_P75','duration_P95','duration_P99']
externalServiceNameList=['AdInsightsMiddleTier','BillingMiddleTier','CampaignMiddleTier','CampaignAggregatorService','ClientCenterMiddleTier','MessageCenterMiddleTier','ReportingMiddleTier']
densityLength = 1000

def connectDB():
    server = 'tcp:ucmloggingdatawarehouse.database.windows.net,1433' 
    database = 'ucmloggingdatawarehouse' 
    username = 'loggingDW_readonly' 
    password = 'Read@Only123' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def getRequestUrlList(cursor, externalServiceName):
    requestUrlList = []
    sqlQuery = "SELECT DISTINCT requestUrl " + \
            "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
            "WHERE externalServiceName='" + externalServiceName + "'"
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    while row:
        requestUrlList.append(row[0])
        row = cursor.fetchone()
    return requestUrlList

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

def getDensity(origin):
    xmin = origin.min()
    xmax = origin.max()
    xs = np.linspace(xmin*0.5,xmax*1.2,densityLength)
    densityFunc= stats.gaussian_kde(origin)
    ys = densityFunc(xs)
    density = {"x":xs,"y":ys}
    return density

def gaussFunc(par, t):
    return (par[0]/par[1])*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2)))

def errFunc(par, t, y):
    err= y - gaussFunc(par,t)
    return err

def getP0(density):
    xs = density['x']
    ys = density['y']
    indices= peakutils.indexes(-ys)
    indices= np.append(indices,0)
    indices= np.append(indices,densityLength-1)
    muEst = max(ys)
    valleies = xs[indices]
    dis = abs(valleies-muEst)
    sEst = (min(dis)/2)
    p0 = [1/np.sqrt(2*np.pi)/sEst, sEst, muEst]
    return p0

def twoGaussFunc(par, t):
    return (par[0]/par[1])*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2))) + \
            (par[3]/par[4])*np.exp(-np.power(t-par[5],2)/(2*np.power(par[4],2)))
    
def errTwoGaussFunc(par, t, y):
    err= y - twoGaussFunc(par,t)
    return err

def getTwoGaussP0(density):
    xs = density['x']
    ys = density['y']
    peakIndices = peakutils.indexes(ys)
    while (len(peakIndices) > 2):
        peaks = ys[peakIndices]
        peakIndices = np.delete(peakIndices,np.argmin(peaks))
    muEst = xs[peakIndices]
    sEst = []
    valleyIndices= peakutils.indexes(-ys)
    valleyIndices= np.append(valleyIndices,0)
    valleyIndices= np.append(valleyIndices,densityLength-1)
    valleies = xs[valleyIndices]
    for mu in muEst:
        dis = abs(valleies-mu)
        sEst.append(min(dis)/2)
    p0 = [1/np.sqrt(2*np.pi)/sEst[0], sEst[0], muEst[0], \
         1/np.sqrt(2*np.pi)/sEst[1], sEst[1], muEst[1]]
    return p0

def saveChart(density,origin,anomaly,figName):
    fig= plt.figure(figsize = (20, 7))
    plt.subplot(1,2,1)
    plt.plot(density['x'],density['y'])
    plt.plot(density['x'],density['yEst'])
    plt.subplot(1,2,2)
    plt.plot(origin.startDayHour, origin.duration_P75)
    plt.plot(anomaly.startDayHour, anomaly.duration_P75,'ro')
    fig.savefig('{}{}.png'.format(figName,origin.iloc[-1].startDayHour))
    plt.close(fig)

def getThreshold(pEst):
    mu= pEst[0][2]
    s= pEst[0][1]
    return mu+2*s

cursor = connectDB()
for externalServiceName in externalServiceNameList:
    requestUrlList = getRequestUrlList(cursor, externalServiceName)
    for requestUrl in requestUrlList:
        data = loadData(cursor, externalServiceName, requestUrl)
        period = 120
        endIndex = len(data)
        for i in range(period,endIndex):
            t0= i-period
            origin = data[t0:i]
            perf = origin.duration_P75
            density = getDensity(perf)
            if (len(peakutils.indexes(density['y'])) > 1):
                p0 = getTwoGaussP0(density)
                pEst= leastsq(errTwoGaussFunc, p0, args = (density['x'], density['y']))
                density['yEst'] = twoGaussFunc(pEst[0],density['x'])
            else:
                p0 = getP0(density)
                pEst= leastsq(errFunc, p0, args = (density['x'], density['y']))
                density['yEst'] = gaussFunc(pEst[0],density['x'])
            threshold = getThreshold(pEst)
            anomaly = origin[perf>threshold]
            request = requestUrl[requestUrl.rfind('/')+1:]
            saveChart(density, origin, anomaly,'{}_{}_'.format(externalServiceName,request))
            #if (anomaly.iloc[-1].startDayHour == origin.iloc[-1].startDayHour):
            #    saveChart(density, origin, anomaly, 'Anomaly_{}_{}_'.format(externalServiceName,request))
                #createIcM
 