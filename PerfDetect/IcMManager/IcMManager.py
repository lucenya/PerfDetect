import logging
import base64
import pandas as pd
from retry import retry
from . import icm_client
from . import credentials
#import icm_client
#import credentials
#import incident
#from os import path
#import sys
#sys.path.append(path.abspath('../'))
#from icm import icm_client

host = credentials.ppe_host
cert = credentials.primary_cert
key = credentials.primary_key
connector_id = credentials.ppe_connector_id

class IcMManager(object):
    def __init__(self, mongoDB):
        self.icm_api = icm_client.ICMApi(icm_host=host, cert=cert, key=key, connector_id=connector_id, debug=True)
        self.mongoDB = mongoDB

    def CreatOrUpdateIcM(self, perfKey, title, descriptionEntryText, attachedFile):
        incidentId = self.mongoDB.GetIncident(perfKey)
        if (incidentId != -1 and self.isIcMActive(incidentId)):
            self.updateIcM(incidentId, descriptionEntryText)            
        else:
            incidentId = self.createIcM(title, descriptionEntryText)
            self.mongoDB.SaveIncident(perfKey, incidentId)
        self.addAttachment(incidentId, attachedFile)
        return incidentId

    def createIcM(self, title, descriptionEntryText):
        incident = self.icm_api.new_incident()
        incident['DescriptionEntries'][0]['DescriptionEntry']['Text'] = descriptionEntryText
        incident['Title'] = title
        incident['Severity'] = 4
        result = self.icm_api.create_incident(incident=incident)
        return result[0]

    def getIcM(self, incidentId):
        incident = self.icm_api.get_incident(incident_id=incidentId)
        return incident

    def updateIcM(self, incidentId, newDescriptionEntryText):
        body = {'NewDescriptionEntry': {'Text': newDescriptionEntryText,
                                'RenderType': 'Plaintext'}}
        result = self.icm_api.update_incident(incident_id=incidentId, body=body)
        return result

    @retry(tries=5, delay=2)
    def addAttachment(self, incidentId, fileName):
        with open(fileName, 'rb') as attachment_file:
            content = base64.b64encode(attachment_file.read())
        body = {'Attachment': {'Filename': fileName, 'ContentsBase64': content.decode('utf-8')}}
        result = self.icm_api.update_incident(incident_id=incidentId, body=body, entity='CreateAttachment')
        return result
        
    def isIcMActive(self, incidentId):
        incident = self.getIcM(incidentId)
        status = incident['Status']
        return status == 'Active' or status == 'Correlating'

            


#IcM = IcMManager()
#IcM.isIcMExist('[Perf]CampaignAggregatorService under All drops')
#IcM.CreatOrUpdateIcM('a', 'title', 'descriptionEntryText', 'CampaignAggregatorService_All_2017-09-06.png')
#IcM.getIcM('51749190')
#IcM.addHitCount('51749190')
##IcMRes = IcM.createIcM('Title','Summary')
##IcM.addAttachment(IcMRes[0],'CampaignAggregatorService_AccountPerformance_2017-09-05.png')

#IcM.addAttachment('51749190','CampaignAggregatorService_All_2017-09-06.png')


#filename = 'attachment.txt'
#icm_api = icm_client.ICMApi(icm_host='icm.ad.msoppe.msft.net', cert="./IcMManager/cert.pem", key="./IcMManager/key.pem", connector_id='3ef3e081-28c4-4bb3-8c33-d2c523194103', debug=True)

#with open(filename, 'rb') as attachment_file:
#    content = base64.b64encode(attachment_file.read())

#body = {'Attachment': {'Filename': filename, 'ContentsBase64': content.decode('utf-8')}}

#incident = icm_api.update_incident(incident_id='51749190', body=body, entity='CreateAttachment')

#print(incident)