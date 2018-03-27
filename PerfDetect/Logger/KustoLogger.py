import csv
from datetime import datetime
from azure.kusto.ingest import KustoIngestClient, IngestionProperties, FileDescriptor, BlobDescriptor, DataFormat
from . import credentials
from . import environment

class KustoLogType(object):
    perf_normal = "PerfNormal"
    perf_anomaly = 'PerfAnomaly'
    read_database_error = "ReadDatabaseError"
    fit_density_error = "FitDensityError"
    call_icm_error = "CallIcMError"

class KustoLogger(object):
    _log_keys = ["TIMESTAMP", "PreciseTimeStamp", "Tenant", "Role", "RoleInstance", "Level", "ProviderGuid",
                 "ProviderName", "IncidentId", "Status", "LogType", "Context"]

    def __init__(self):
        self.ingest_client = KustoIngestClient(environment.kusto_ppe_ingest_connection,
                                               client_id=credentials.kusto_application_id,
                                               client_secret=credentials.kusto_application_key)
        self.properties = IngestionProperties(database="BingAdsUCM", table="PerfIcMAlertEvent",dataFormat=DataFormat.csv)
        self.log_buffer_file = "kusto_log_buffer.csv"

    def PerfNormal(self, externalServiceName, requestUrl, detectedDate):
        context = {
            "ExternalServiceName": externalServiceName,
            "RequestUrl": requestUrl,
            "DetectedDate": detectedDate            
        }
        self._write_log(log_type=KustoLogType.perf_normal, is_succeed=True, incident_id='',
                        context=context, push_remote=True)

    def PerfAnomaly(self, externalServiceName, requestUrl, detectedDate, incident_id, log):
        context = {
            "ExternalServiceName": externalServiceName,
            "RequestUrl": requestUrl,
            "DetectedDate": detectedDate,
            "IncidentId": incident_id,
            "Log": log
        }
        self._write_log(log_type=KustoLogType.perf_anomaly, is_succeed=True, incident_id=incident_id,
                        context=context, push_remote=True)

    def ExecuteError(self, logType, externalServiceName, requestUrl, detectedDate, log):
        context = {
            "ExternalServiceName": externalServiceName,
            "RequestUrl": requestUrl,
            "DetectedDate": detectedDate,
            "Log": log
        }
        self._write_log(log_type=logType, is_succeed=False, incident_id='',context=context, push_remote=True)
        
    def _write_log(self, log_type: object, is_succeed: object, incident_id: object = None, context: object = None,
                   push_remote: object = False):
        now = str(datetime.utcnow())
        log = {
            "TIMESTAMP": now,
            "PreciseTimeStamp": now,
            "Tenant": "Production-Container-CentralUS",
            "Role": "Microsoft.UCM.PerfIcMAlert",
            "RoleInstance": "Microsoft.UCM.PerfIcMAlert_IN_1",
            "Level": 4,
            "ProviderGuid": "41d378e3-f3fc-5079-4f2d-69dc57bf7f41",
            "ProviderName": "PyEventSource",
            "IncidentId": incident_id,
            "Status": "Success" if is_succeed else "Failure",
            "LogType": log_type,
            "Context": str(context)
        }

        with open(self.log_buffer_file, "a+") as file:
            f_csv = csv.DictWriter(file, self._log_keys)
            f_csv.writerow(log)
        if push_remote is True:
            self._push_log()

    def _push_log(self):
        self.ingest_client.ingest_from_multiple_files([self.log_buffer_file], delete_sources_on_success=True,
                                                       ingestion_properties=self.properties)
        # clean buffer
        open(self.log_buffer_file, "w").close()


if __name__ == "__main__":
    KustoLogger()._write_log("JobExecutionError", False, context="Testing", push_remote=True)
