from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import MSsqlSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import pandas as pd
import json, pyodbc

# ViewSets define the view behavior.

""" Retrieve Database List from MS SQL Server """

class MSsql_ListSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = MSsqlSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = MSsqlSerializer(data=request.body)
            MSsql_server = request.data.get("MSsql_server", "")
            data = {
            }
            try:
                drivers = [item for item in pyodbc.drivers()]
                driver = drivers[3]
                MSsql_conn = pyodbc.connect('Driver={};'
                'Server={};'
                'Trusted_Connection=yes;'
                'timeout=1;'.format(driver,MSsql_server))

                cursor = MSsql_conn.cursor()
                mssql_file = pd.io.sql.read_sql('EXEC sp_databases', MSsql_conn)
                MSsql_conn.close()
                database_list = mssql_file['DATABASE_NAME'].to_list()
                data['database_list'] = json.dumps(database_list)
            except pyodbc.Error as err:
              return JsonResponse({'Database Error': str(err)}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Table List from MS SQL Server """

class MSsql_TableSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = MSsqlSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = MSsqlSerializer(data=request.body)
            MSsql_server = request.data.get("MSsql_server", "")
            MSsql_db = request.data.get("MSsql_db", "")
            data = {
            }

            drivers = [item for item in pyodbc.drivers()]
            MSsql_driver = drivers[3]

            MSsql_conn = pyodbc.connect('Driver={};'
            'Server={};'
            'Database={};'
            'Trusted_Connection=yes;'
            'timeout=1;'.format(MSsql_driver,MSsql_server, MSsql_db))

            cursor = MSsql_conn.cursor()
            mssql_file = pd.io.sql.read_sql('SELECT * FROM INFORMATION_SCHEMA.TABLES;', MSsql_conn)
            MSsql_conn.close()
            collection_list = mssql_file['TABLE_NAME'].to_list()
            data['collection_list'] = json.dumps(collection_list)

        return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Data from MS SQL Server"""

class MSsqlViewSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = MSsqlSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = MSsqlSerializer(data=request.body)
            MSsql_server = request.data.get("MSsql_server", "")
            MSsql_db = request.data.get("MSsql_db", "")
            MSsql_table = request.data.get("MSsql_table", "")

            data = {
            }

            drivers = [item for item in pyodbc.drivers()]
            MSsql_driver = drivers[3]

            MSsql_conn = pyodbc.connect('Driver={};'
            'Server={};'
            'Database={};'
            'Trusted_Connection=yes;'
            'timeout=1;'.format(MSsql_driver,MSsql_server,MSsql_db))

            cursor = MSsql_conn.cursor()
            mssql_file = pd.io.sql.read_sql('SELECT * FROM '+MSsql_db+'.dbo.'+MSsql_table, MSsql_conn)
            MSsql_conn.close()

            mssql_json = mssql_file.to_dict("records")

            res = len([ele for ele in mssql_json if isinstance(ele, dict)])
            if str(res) == '0':
                content = {'response_msg': 'This table is Empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                data['file_data'] = json.dumps(mssql_json)

                dtype_list = mssql_file.dtypes.apply(lambda x: x.name).to_list() 
                data['dtype_list'] = json.dumps(dtype_list)

                file_name = 'MsSQL_'+MSsql_table
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, mssql_file)
                data['file_path'] = FileName

        return JsonResponse(data)
