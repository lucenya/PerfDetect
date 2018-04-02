from pymongo import MongoClient
import urllib.parse
#from . import environment

PERF_KEY = "perfKey"
TWO_GAUSS_P = "TwoGaussP"
INCIDENT_ID = "incidentId"

class MongoDB(object):
    def __init__(self):
        uri = "mongodb://perfdetect:asdlkj@mongo/default_db?authSource=perfdetect"
        #uri = "mongodb://perfdetect:asdlkj@127.0.0.1:27017/default_db?authSource=perfdetect"
        self.client = MongoClient(uri)
        self.db = self.client["perfdetect"]
        self.lastTwoGaussP = self.db["lastTwoGaussP"]
        self.icmIncident = self.db["icmIncident"]

    def SaveTwoGaussP(self, perfKey, pValue):
        self.lastTwoGaussP.find_one_and_delete({PERF_KEY: perfKey})
        self.lastTwoGaussP.insert_one({
            PERF_KEY: perfKey,
            TWO_GAUSS_P: pValue
        })

    def GetTwoGaussP(self, perfKey):
        res = self.lastTwoGaussP.find_one({PERF_KEY: perfKey})
        if (res is None):
            return []
        else:
            return res[TWO_GAUSS_P]

    def SaveIncident(self, perfKey, incidentId):
        self.icmIncident.find_one_and_delete({PERF_KEY: perfKey})
        self.icmIncident.insert_one({
            PERF_KEY: perfKey,
            INCIDENT_ID: incidentId
        })

    def GetIncident(self, perfKey):
        res = self.icmIncident.find_one({PERF_KEY: perfKey})
        if (res is None):
            return -1
        else:
            return res[INCIDENT_ID]


#mongoDB = MongoDB()
#mongoDB.SaveIncident("test", 12345)
#mongoDB.GetIncident("test")
#mongoDB.SaveIncident("test", 54321)

#mongoDB.SaveTwoGaussP("test", [1,2,3,4,5,6])
#mongoDB.GetTwoGaussP("test")
#mongoDB.SaveTwoGaussP("test", [2,2,3,4,5,6])
