import pytest
from DataProvider import ExternalServiceCallPerfDataProvider

@pytest.fixture()
def data_provider():
    return ExternalServiceCallPerfDataProvider.ExternalServiceCallPerfDataProvider()

def test_GetPerfData(data_provider):
    df = data_provider.GetPerfData('CampaignAggregatorService', 'All')
    assert 120 == df.shape[0]
    assert 10 == df.shape[1]

def test_GetRequestUrlList(data_provider):
    res = data_provider.GetRequestUrlList('CampaignAggregatorService')
    assert 10 < len(res)

def test_getRequestUrlListSQLQuery(data_provider):
    assert data_provider.getRequestUrlListSQLQuery('CampaignAggregatorService') == "SELECT DISTINCT requestUrl " + \
                                                                    "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day]" + \
                                                                    "WHERE externalServiceName='CampaignAggregatorService'"

def test_getExternalServiceCallSQLQuery(data_provider):
    assert data_provider.getExternalServiceCallSQLQuery('CampaignAggregatorService', 'All') == "SELECT TOP(120) [startDayHour]" + \
                                                                                 ",[externalServiceName]" + \
                                                                                 ",[externalServiceCall]" + \
                                                                                 ",[requestUrl]" + \
                                                                                 ",[numSamples]" + \
                                                                                 ",[maxDuration]" + \
                                                                                 ",[duration_P50]" + \
                                                                                 ",[duration_P75]" + \
                                                                                 ",[duration_P95]" + \
                                                                                 ",[duration_P99]" + \
                                                                                 "FROM [Kusto].[ExternalServiceCallPercentileTrend_Day] " + \
                                                                                 "where externalServiceName = 'CampaignAggregatorService' and " + \
	                                                                             "requestUrl='All' and " + \
	                                                                             "externalServiceCall='All' and " + \
	                                                                             "DATENAME(dw, startDayHour)<>'Saturday' and DATENAME(dw,startDayHour)<>'Sunday' " + \
                                                                                 "order by startDayHour desc"
