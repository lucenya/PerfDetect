import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
from datetime import datetime
from PerfDetect.DataProvider.ExternalServiceCallPerfDataProvider import ExternalServiceCallPerfDataProvider
from PerfDetect.DataProvider.UcmDbPerfDataProvider import UcmDbPerfDataProvider
from PerfDetect.GaussFitting import DensityProvider
from PerfDetect.GaussFitting import OneGaussFitting
from PerfDetect.GaussFitting import TwoGaussFitting
from PerfDetect.IcMManager.IcMManager import IcMManager
from PerfDetect.Logger.KustoLogger import KustoLogger
from PerfDetect.Logger.KustoLogger import KustoLogType
from PerfDetect.MongoDB.MongoDB import MongoDB

class PerfDetect(object):
    def __init__(self, **kwargs):
        self.Logger = KustoLogger()
        self.mongoDB = MongoDB()
        self.IcM = IcMManager(self.mongoDB)
        self.externalServiceDataProvider = ExternalServiceCallPerfDataProvider()
        self.ucmDbDataProvider = UcmDbPerfDataProvider()
        return super().__init__(**kwargs)

    def saveChart(self, density, origin, anomaly, fileName):
        threshold = density['threshold']
        fig= plt.figure(figsize = (20, 7), dpi=40)
        plt.subplot(1,2,1)
        plt.plot(density['x'],density['y'],'b')
        plt.plot(density['x'],density['yEst'], 'y')
        plt.plot([threshold,threshold],[0,max(density['y'])],'r')
        plt.title('Density')
        plt.subplot(1,2,2)
        plt.plot(origin.startDayHour, origin.duration_P75)
        plt.plot(anomaly.startDayHour, anomaly.duration_P75,'ro')
        plt.title('Perf_P75({})'.format(origin.iloc[-1].numSamples))
        fig.savefig(fileName)
        plt.close(fig)

    def saveData(self, origin, fileName):
        origin.to_csv(fileName, index=False)

    def getPerfKey(self, categoryName, requestUrl):
        requestName = requestUrl[requestUrl.rfind('/')+1:]
        return '{}_{}'.format(categoryName,requestName)

    def getDecriptions(self, density, origin, categoryName, requestUrl):
        dataTime = origin.iloc[-1].startDayHour
        curPerf = origin.iloc[-1].duration_P75
        descriptions = {}
        descriptions['IcM_pefKey'] = categoryName
        descriptions['chartFileName'] = '{}_{}.png'.format(self.getPerfKey(categoryName, requestUrl), dataTime)
        descriptions['dataFileName'] = '{}_{}.csv'.format(self.getPerfKey(categoryName, requestUrl), dataTime)
        descriptions['IcM_Title'] = '[Perf]{} drops'.format(categoryName)
        descriptions['IcM_Description'] = ('[Perf]{} under {} drops in {}.'.format(categoryName, requestUrl, dataTime) + '\n' + 
                                          'Current Perf is {} and the threshold is {}'.format(curPerf, density['threshold']))
        return descriptions

    def startDetect(self, categoryName, requestUrl, origin):
        perfKey = self.getPerfKey(categoryName, requestUrl)
        detectedDate = origin.iloc[-1].startDayHour        
        perf = origin.duration_P75
        try:
            density = DensityProvider.GetDensity(perf)
            if (DensityProvider.IsOneMorePeak(density)):
                density = TwoGaussFitting.Fitting(density, perfKey, self.mongoDB)
            else:
                density = OneGaussFitting.Fitting(density)
        except Exception as e:
            self.Logger.ExecuteError(KustoLogType.fit_density_error, categoryName, requestUrl, detectedDate, "Unexpected error: {}".format(e))
            return

        anomaly = origin[origin.duration_P75 > density['threshold']]
        if ((not anomaly.empty) and  anomaly.iloc[-1].startDayHour == detectedDate):
            descriptions = self.getDecriptions(density, origin, categoryName, requestUrl)
            self.saveChart(density, origin, anomaly, descriptions['chartFileName'])
            self.saveData(origin, descriptions['dataFileName'])
            try:
                incidentId = self.IcM.CreatOrUpdateIcM(descriptions['IcM_pefKey'], descriptions['IcM_Title'], descriptions['IcM_Description'], descriptions['chartFileName'], descriptions['dataFileName'])
                self.Logger.PerfAnomaly(categoryName, requestUrl, detectedDate, incidentId, descriptions['IcM_Description'])
            except Exception as e:
                self.Logger.ExecuteError(KustoLogType.call_icm_error, categoryName, requestUrl, detectedDate, "Unexpected error: {}".format(e))            
        else:
            self.Logger.PerfNormal(categoryName, requestUrl, detectedDate)

    def DetectExternalServiceCall(self):
        print('External Service Call Perf Detect Start {}'.format(datetime.now()))
        for externalServiceName in self.externalServiceDataProvider.GetExternalServiceNameList():
            startDate = self.externalServiceDataProvider.GetStartDate(externalServiceName)
            requestUrlList = self.externalServiceDataProvider.GetRequestUrlList(externalServiceName, startDate)
            for requestUrl in requestUrlList:
                print("\nStart Detecting {} {}".format(externalServiceName, requestUrl))
                origin = self.externalServiceDataProvider.GetPerfData(externalServiceName, requestUrl)
                if (origin.shape[0] != 120 or origin.iloc[0].startDayHour != startDate):
                    print("{} doesn't contain last 120 weekday data".format(requestUrl))
                    continue
                self.startDetect(externalServiceName, requestUrl, origin)
        print('External Service Call Perf Detect End {}'.format(datetime.now()))

    def DetectUcmDb(self):
        print('UCM DB Perf Detect Start {}'.format(datetime.now()))
        for externalServiceName in self.ucmDbDataProvider.GetExternalServiceNameList():
            startDate = self.ucmDbDataProvider.GetStartDate(externalServiceName)
            externalServiceCallList = self.ucmDbDataProvider.GetExternalServiceCallList(externalServiceName, startDate)            
            for externalServiceCall in externalServiceCallList:
                print("\nStart Detecting {} {}".format(externalServiceName, externalServiceCall))
                origin = self.ucmDbDataProvider.GetPerfData(externalServiceName, externalServiceCall)
                if (origin.shape[0] != 120 or origin.iloc[0].startDayHour != startDate):
                    print("{} doesn't contain last 120 weekday data".format(externalServiceCall))
                    continue
                self.startDetect(externalServiceName, externalServiceCall, origin)
        print('UCM DB Perf Detect End {}'.format(datetime.now()))

    #def DetectUcmDb(self):
    #    print('UCM DB Perf Detect Start {}'.format(datetime.now()))
    #    for externalServiceName in self.ucmDbDataProvider.GetExternalServiceNameList():
    #        startDate = self.ucmDbDataProvider.GetStartDate(externalServiceName)
    #        externalServiceCallList = self.ucmDbDataProvider.GetExternalServiceCallList(externalServiceName, startDate)            
    #        for externalServiceCall in externalServiceCallList:
    #            print("\nStart Detecting {} {}".format(externalServiceName, externalServiceCall))
    #            if (not self.isExpectedExternalServiceCall(externalServiceCall)):
    #                print("Ignore")
    #                continue
    #            data = self.ucmDbDataProvider.GetPerfData(externalServiceName, externalServiceCall)
    #            period = 120
    #            endIndex = len(data)
    #            for i in range(period,endIndex):
    #                t0 = i - period
    #                origin = data[t0:i]
    #                self.startDetect(externalServiceName, externalServiceCall, origin)
    #    print('UCM DB Perf Detect End {}'.format(datetime.now()))


#perfdetect = PerfDetect()
#perfdetect.DetectExternalServiceCall()
    