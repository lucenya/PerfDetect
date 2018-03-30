from . import SqlConnector

externalServiceNameList=['AdInsightsMiddleTier','BillingMiddleTier','CampaignMiddleTier','CampaignAggregatorService','ClientCenterMiddleTier','MessageCenterMiddleTier','ReportingMiddleTier']

class ExternalServiceCallPerfDataProvider(object):

    def __init__(self):
        self.sqlConnect = SqlConnector.SqlConnector()

    def GetPerfData(self, externalServiceName, requestUrl):
        sqlQuery = self.getExternalServiceCallSQLQuery(externalServiceName, requestUrl)
        return self.sqlConnect.GetDataAsDataFrame(sqlQuery)

    def GetRequestUrlList(self, externalServiceName):
        sqlQuery = self.getRequestUrlListSQLQuery(externalServiceName)
        return self.sqlConnect.GetDataAsList(sqlQuery)
    
    def GetStartDate(self, externalServiceName):
        sqlQuery = self.getExternalServiceCallSQLQuery(externalServiceName, 'All')
        df = self.sqlConnect.GetDataAsDataFrame(sqlQuery)
        return df.iloc[0].startDayHour

    def getRequestUrlListSQLQuery(self, externalServiceName):
        sqlQuery = "SELECT DISTINCT requestUrl " + \
                "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
                "WHERE externalServiceName='" + externalServiceName + "'"
        return sqlQuery

    def getExternalServiceCallSQLQuery(self, externalServiceName, requestUrl):
        columnNames = ""
        for name in SqlConnector.columnNameList:
            columnNames = columnNames + "[" + name + "],"
        columnNames = columnNames[0:len(columnNames)-1]
        sqlQuery = "SELECT TOP(120) " + columnNames + \
                "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day] " + \
                "where externalServiceName = '" + externalServiceName +"' and " + \
                "requestUrl='" + requestUrl + "' and " + \
                "externalServiceCall='All' and " + \
                "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday' " + \
                "order by startDayHour desc"
        return sqlQuery


