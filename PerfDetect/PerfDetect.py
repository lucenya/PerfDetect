import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
from datetime import datetime
from DataProvider.ExternalServiceCallPerfDataProvider import *
from GaussFitting import *
from IcMManager.IcMManager import IcMManager
from Logger.KustoLogger import *

def saveChart(density,origin,anomaly,fileName):
    threshold = density['threshold']
    fig= plt.figure(figsize = (20, 7), dpi=40)
    plt.subplot(1,2,1)
    plt.plot(density['x'],density['y'],'b')
    #plt.plot(density['x'],density['y0Est'], 'g')
    plt.plot(density['x'],density['yEst'], 'y')
    plt.plot([threshold,threshold],[0,max(density['y'])],'r')
    plt.title('Density')
    plt.subplot(1,2,2)
    plt.plot(origin.startDayHour, origin.duration_P75)
    plt.plot(anomaly.startDayHour, anomaly.duration_P75,'ro')
    plt.title('Perf_P75')
    fig.savefig(fileName)
    plt.close(fig)

def getDecriptions(density, origin, externalServiceName, requestUrl):
    dataTime = origin.iloc[-1].startDayHour
    curPerf = origin.iloc[-1].duration_P75
    requestName = requestUrl[requestUrl.rfind('/')+1:]
    decriptions = {}
    decriptions['fileName'] = '{}_{}_{}.png'.format(externalServiceName,requestName,dataTime)
    decriptions['IcM_PerfKey'] = '{}_{}'.format(externalServiceName,requestName)
    decriptions['IcM_Title'] = '[Perf]{} under {} drops'.format(externalServiceName, requestName)
    decriptions['IcM_Description'] = ('[Perf]{} under {} drops in {}.'.format(externalServiceName, requestUrl, dataTime) + '\n' + 
                                      'Current Perf is {} and the threshold is {}'.format(curPerf, density['threshold']))
    return decriptions

Logger = KustoLogger()
IcM = IcMManager()
externalServiceDataProvider = ExternalServiceCallPerfDataProvider()
print('Perf Detect Start {}'.format(datetime.now()))
for externalServiceName in ['CampaignAggregatorService']:
    requestUrlList = externalServiceDataProvider.GetRequestUrlList(externalServiceName)
    startDate = externalServiceDataProvider.GetStartDate(externalServiceName)
    for requestUrl in requestUrlList:
        origin = externalServiceDataProvider.GetPerfData(externalServiceName, requestUrl)
        if (origin.shape[0] != 120 or origin.iloc[0].startDayHour != startDate):
            print("{} doesn't contain last 120 weekday data".format(requestUrl))
            continue

        detectedDate = origin.iloc[-1].startDayHour        
        perf = origin.duration_P75
        try:
            density = DensityProvider.GetDensity(perf)
            if (DensityProvider.IsOneMorePeak(density)):
                density = TwoGaussFitting.Fitting(density, '{}_{}'.format(externalServiceName, requestUrl[requestUrl.rfind('/')+1:]) )
            else:
                density = OneGaussFitting.Fitting(density)
        except Exception as e:
            Logger.ExecuteError(KustoLogType.fit_density_error, externalServiceName, requestUrl, detectedDate, "Unexpected error: {}".format(e))
            continue

        anomaly = origin[origin.duration_P75 > density['threshold']]
        if ((not anomaly.empty) and  anomaly.iloc[-1].startDayHour == detectedDate):
            descriptions = getDecriptions(density, origin, externalServiceName, requestUrl)
            saveChart(density, origin, anomaly, descriptions['fileName'])
            try:
                incidentId = IcM.CreatOrUpdateIcM(descriptions['IcM_PerfKey'], descriptions['IcM_Title'], descriptions['IcM_Description'], descriptions['fileName'])
                Logger.PerfAnomaly(externalServiceName, requestUrl, detectedDate, incidentId, descriptions['IcM_Description'])
            except Exception as e:
                Logger.ExecuteError(KustoLogType.call_icm_error, externalServiceName, requestUrl, detectedDate, "Unexpected error: {}".format(e))            
        else:
            Logger.PerfNormal(externalServiceName, requestUrl, detectedDate)
print('Perf Detect Finish {}'.format(datetime.now()))




#sqlConnector = SqlConnector()

#for externalServiceName in externalServiceNameList:
#    requestUrlList = getRequestUrlList(cursor, externalServiceName)
#    for requestUrl in requestUrlList:
#        data = loadData(cursor, externalServiceName, requestUrl)
#        period = 120
#        endIndex = len(data)
#        lastTwoGaussP = []
#        for i in range(period,endIndex):
#            t0= i-period
#            origin = data[t0:i]
#            perf = origin.duration_P75
#            density = getDensity(perf)
#            if (len(peakutils.indexes(density['y'])) > 1):
#                p0 = getTwoGaussP0(density,lastTwoGaussP)
#                pEst= least_squares(errTwoGaussFunc, p0, args = (density['x'], density['y']), gtol=1e-9)
#                density['yEst'] = twoGaussFunc(pEst.x,density['x'])
#                lastTwoGaussP = abs(pEst.x)
#            else:
#                p0 = getP0(density)
#                pEst= least_squares(errFunc, p0, args = (density['x'], density['y']))
#                density['yEst'] = gaussFunc(pEst.x,density['x'])
#            threshold = getThreshold(pEst.x)
#            anomaly = origin[perf>threshold]
#            request = requestUrl[requestUrl.rfind('/')+1:]
#            saveChart(density, origin, anomaly,'{}_{}_'.format(externalServiceName,request),pEst)
#            #if (anomaly.iloc[-1].startDayHour == origin.iloc[-1].startDayHour):
#            #    saveChart(density, origin, anomaly, 'Anomaly_{}_{}_'.format(externalServiceName,request))
#                #createIcM

#externalServiceName = 'AdInsightsMiddleTier'
#requestUrl = 'https://api.ucm.bingads.microsoft.com/api/v2/DataTable/AccountTiles'
#data = loadData(cursor, externalServiceName, requestUrl)
#period = 120
#endIndex = len(data)
#lastTwoGaussP = []
#for i in range(period+58,endIndex):
#    t0= i-period
#    origin = data[t0:i]
#    perf = origin.duration_P75
#    density = getDensity(perf)
#    if (len(peakutils.indexes(density['y'])) > 1):
#        p0 = getTwoGaussP0(density,lastTwoGaussP)
#        pEst= least_squares(errTwoGaussFunc, p0, args = (density['x'], density['y']), gtol=1e-9)
#        density['yEst'] = twoGaussFunc(pEst.x,density['x'])
#        lastTwoGaussP = abs(pEst.x)
#    else:
#        p0 = getP0(density)
#        pEst= least_squares(errFunc, p0, args = (density['x'], density['y']))
#        density['yEst'] = gaussFunc(pEst.x,density['x'])
#    threshold = getThreshold(pEst.x)
#    anomaly = origin[perf>threshold]
#    request = requestUrl[requestUrl.rfind('/')+1:]
#    saveChart(density, origin, anomaly,'{}_{}_'.format(externalServiceName,request),pEst)
#    #if (anomaly.iloc[-1].startDayHour == origin.iloc[-1].startDayHour):
#    #    saveChart(density, origin, anomaly, 'Anomaly_{}_{}_'.format(externalServiceName,request))
#        #createIcM
 

    