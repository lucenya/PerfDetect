import pytest
from DataProvider import SqlConnector

@pytest.fixture()
def sql_connector():
    return SqlConnector.SqlConnector()

def test_GetDataAsDataFrame(sql_connector):
    sqlQuery = "SELECT TOP(1) [startDayHour],[externalServiceName]" + \
                "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
                "where externalServiceName = 'CampaignAggregatorService' and " + \
                "requestUrl='All' and " + \
                "externalServiceCall='All' and " + \
                "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday'" + \
                "order by startDayHour desc"
    df = sql_connector.GetDataAsDataFrame(sqlQuery)
    assert 1 == df.shape[0]
    assert 2 == df.shape[1]

def test_GetDataAsList(sql_connector):
    sqlQuery = "select @@version"
    res = sql_connector.GetDataAsList(sqlQuery)
    assert 1 == len(res)
    assert -1 != res[0].find("Microsoft")


