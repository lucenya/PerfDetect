import pytest
from IcMManager import IcMManager
from IcMManager import credentials
from os import path

@pytest.fixture()
def icm_manager():
    IcMManager.host = credentials.ppe_host
    IcMManager.cert = ".\\IcMManager\\cert\\cert.pem"
    IcMManager.key = '.\\IcMManager\\cert\key.pem'
    IcMManager.connector_id = credentials.ppe_connector_id
    IcMManager.perf_icm_file_path = ".\\Test\\perfIcM_test.csv"
    return IcMManager.IcMManager()

def test_CreatOrUpdateIcM_new(icm_manager):
    assert 52348154 != icm_manager.CreatOrUpdateIcM("PerfKey", "Test_Title", "Description_Test", ".\\Test\\testAttach.txt")

def test_CreatOrUpdateIcM_exist(icm_manager):
    assert 52348154 == icm_manager.CreatOrUpdateIcM("test", "Test_Title", "Description_Test", ".\\Test\\testAttach.txt")

def test_getIcM(icm_manager):
    incident = icm_manager.getIcM(52348154)
    assert "Test_Title" == incident['Title']
    assert 4 == incident["Severity"]

def test_updateIcM(icm_manager):
    assert "" == icm_manager.updateIcM(52348154, "Description_new")

def test_isIcMActive(icm_manager):
    assert True == icm_manager.isIcMActive(52348154)