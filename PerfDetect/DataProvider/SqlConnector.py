import pyodbc 
import pandas as pd

columnNameList = ['startDayHour','externalServiceName','externalServiceCall','requestUrl','numSamples','maxDuration','duration_P50','duration_P75','duration_P95','duration_P99']

class SqlConnector:    

    def __init__(self, **kwargs):
        self.cursor = self.connectDB();

    def connectDB(self):
        server = 'tcp:ucmloggingdatawarehouse.database.windows.net,1433' 
        database = 'ucmloggingdatawarehouse' 
        username = 'loggingDW_readonly' 
        password = 'Read@Only123' 
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        return cursor

    def GetDataAsDataFrame(self, sqlQuery):
        self.cursor.execute(sqlQuery)
        df = pd.DataFrame()
        row = self.cursor.fetchone()
        while row:
            rowAsList = [d for d in row]
            dfRow = pd.DataFrame([rowAsList])
            df = df.append(dfRow)
            row = self.cursor.fetchone()
        df = df.rename(columns=lambda x: columnNameList[x])
        df = df.sort_values(by=[columnNameList[0]])
        return df

    def GetDataAsList(self, sqlQuery):        
        self.cursor.execute(sqlQuery)
        requestUrlList = []
        row = self.cursor.fetchone()
        while row:
            requestUrlList.append(row[0])
            row = self.cursor.fetchone()
        return requestUrlList


