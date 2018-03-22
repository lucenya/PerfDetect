import matplotlib.pyplot as plt
import sys
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
    decriptions['IcM_Description'] = ('[Perf]{} under {} drops.'.format(externalServiceName, requestUrl) + '\n' + 
                                      'Current Perf is {} and the threshold is {}'.format(curPerf, density['threshold']))
    return decriptions

def createIcMAlert(density, origin, anomaly, externalServiceName, requestUrl):
    requestName = requestUrl[requestUrl.rfind('/')+1:]
    fileName = '{}_{}_{}.png'.format(externalServiceName,requestName,origin.iloc[-1].startDayHour)
    saveChart(density, origin, anomaly, fileName)
    
Logger = KustoLogger()
IcM = IcMManager()
externalServiceDataProvider = ExternalServiceCallPerfDataProvider()
for externalServiceName in ['CampaignAggregatorService']:
    requestUrlList = externalServiceDataProvider.GetRequestUrlList(externalServiceName)
    for requestUrl in ['All']:
        data = externalServiceDataProvider.GetPerfData(externalServiceName, requestUrl)
        period = 120
        endIndex = len(data)
        lastTwoGaussP = []
        for i in range(period,endIndex):
            t0= i-period
            origin = data[t0:i]
            detectedDate = origin.iloc[-1].startDayHour
            perf = origin.duration_P75
            try:
                density = DensityProvider.GetDensity(perf)
                if (DensityProvider.IsOneMorePeak(density)):
                    density = TwoGaussFitting.Fitting(density, lastTwoGaussP)
                    lastTwoGaussP = density['param']
                else:
                    density = OneGaussFitting.Fitting(density)
            except:
                Logger.ExecuteError(KustoLogType.fit_density_error, externalServiceName, requestUrl, detectedDate, "Unexpected error: {}".format(sys.exc_info()[0]))

            anomaly = origin[origin.duration_P75 > density['threshold']]
            if (anomaly.iloc[-1].startDayHour == detectedDate):
                descriptions = getDecriptions(density, origin, externalServiceName, requestUrl)
                saveChart(density, origin, anomaly, descriptions['fileName'])
                try:
                    incidentId = IcM.CreatOrUpdateIcM(descriptions['IcM_PerfKey'], descriptions['IcM_Title'], descriptions['IcM_Description'], descriptions['fileName'])
                except:
                    Logger.ExecuteError(KustoLogType.call_icm_error, externalServiceName, requestUrl, detectedDate, "Unexpected error: {}".format(sys.exc_info()[0]))
                Logger.PerfAnomaly(externalServiceName, requestUrl, detectedDate, incidentId, descriptions['IcM_Description'])
            else:
                Logger.PerfNormal(externalServiceName, requestUrl, detectedDate)





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
 

    