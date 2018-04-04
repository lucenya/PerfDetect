from . import SqlConnector

externalServiceNameList=['AdInsightsMiddleTier','BillingMiddleTier','CampaignMiddleTier','CampaignAggregatorService','ClientCenterMiddleTier','MessageCenterMiddleTier','ReportingMiddleTier']

class ExternalServiceCallPerfDataProvider(object):

    def __init__(self):
        self.sqlConnect = SqlConnector.SqlConnector()

    def GetExternalServiceNameList(self):
        return externalServiceNameList

    def GetPerfData(self, externalServiceName, requestUrl):
        sqlQuery = self.getExternalServiceCallSQLQuery(externalServiceName, requestUrl)
        return self.sqlConnect.GetDataAsDataFrame(sqlQuery, SqlConnector.columnNameList)

    def GetRequestUrlList(self, externalServiceName, startDate):
        sqlQuery = self.getRequestUrlListSQLQuery(externalServiceName, startDate)
        return self.sqlConnect.GetDataAsList(sqlQuery)
    
    def GetStartDate(self, externalServiceName):
        sqlQuery = self.getExternalServiceCallSQLQuery(externalServiceName, 'All')
        df = self.sqlConnect.GetDataAsDataFrame(sqlQuery, SqlConnector.columnNameList)
        return df.iloc[0].startDayHour

    def getRequestUrlListSQLQuery(self, externalServiceName, startDate):
        sqlQuery = "SELECT DISTINCT requestUrl " + \
                "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
                "WHERE externalServiceName='" + externalServiceName + "' and " + \
                "requestUrl not like '%-%' and requestUrl not like '%?%' and " + \
                "externalServiceCall='All' and " + \
                "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday' and " + \
                "startDayHour>='" + startDate.strftime("%Y-%m-%d") + "'"
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


