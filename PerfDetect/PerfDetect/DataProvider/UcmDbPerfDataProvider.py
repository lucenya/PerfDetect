from . import SqlConnector

externalServiceNameList=['UcmDbConn', 'UcmTicketingDbConn', 'UcmBusinessReportingDbConn', 'UcmStagingConn']

class UcmDbPerfDataProvider(object):    
    def __init__(self):
        self.sqlConnect = SqlConnector.SqlConnector()

    def GetExternalServiceNameList(self):
        return externalServiceNameList

    def GetPerfData(self, externalServiceName, externalServiceCall):
        sqlQuery = self.getExternalServiceCallSQLQuery(externalServiceName, externalServiceCall)
        return self.sqlConnect.GetDataAsDataFrame(sqlQuery)

    def GetExternalServiceCallList(self, externalServiceName, startDate):
        sqlQuery = self.getExternalServiceCallListQuery(externalServiceName, startDate)
        return self.sqlConnect.GetDataAsList(sqlQuery)

    def GetStartDate(self, externalServiceName):
        sqlQuery = self.getExternalServiceCallSQLQuery(externalServiceName, 'All')
        df = self.sqlConnect.GetDataAsDataFrame(sqlQuery)
        return df.iloc[0].startDayHour

    def getExternalServiceCallListQuery(self, externalServiceName, startDate):
        sqlQuery = "SELECT DISTINCT externalServiceCall " + \
                "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
                "WHERE externalServiceName='" + externalServiceName + "' and " + \
                "requestUrl='All' and " + \
                "(externalServiceCall='All' or externalServiceCall like '%]%') and " +\
                "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday' and " + \
                "startDayHour>='" + startDate.strftime("%Y-%m-%d") + "'"
        return sqlQuery

    def getExternalServiceCallSQLQuery(self, externalServiceName, externalServiceCall):
        columnNames = ""
        for name in SqlConnector.columnNameList:
            columnNames = columnNames + "[" + name + "],"
        columnNames = columnNames[0:len(columnNames)-1]
        sqlQuery = "SELECT TOP(120) " + columnNames + \
                "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day] " + \
                "where externalServiceName = '" + externalServiceName +"' and " + \
                "requestUrl='All' and " + \
                "externalServiceCall='" + externalServiceCall + "' and " + \
                "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday' " + \
                "order by startDayHour desc"
        return sqlQuery
