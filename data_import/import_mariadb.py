from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import mariadbSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import mysql.connector as database
from mysql.connector.errors import Error
import pandas as pd
import json

# ViewSets define the view behavior.

""" Retrieve Database List from Mariadb """

class mariadb_ListSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mariadbSerializer
    
    def list(self, request):
        return Response("GET API")

    def create(self, request):
        
        if request.method == "POST":
            serializer = mariadbSerializer(data=request.body)
            maria_host = request.data.get("maria_host", "")
            maria_user = request.data.get("maria_user", "")
            maria_pass = request.data.get("maria_pass", "")
            data = {
            }
            try:
                maria_conn = database.connect(
                    user=maria_user,
                    password=maria_pass,
                    host=maria_host)

                maria_file = pd.io.sql.read_sql('SHOW DATABASES', maria_conn)
                maria_conn.close()
                database_list = maria_file['Database'].to_list()
                data['database_list'] = json.dumps(database_list)
            except database.Error as err:
                return JsonResponse({'Database Error': str(err)}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse(data)
 
# =============================================================================================================================

""" Retrieve Table List from Mariadb """

class mariadb_TableSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mariadbSerializer
    
    def list(self, request):
        return Response("GET API")

    def create(self, request):
        
        if request.method == "POST":
            serializer = mariadbSerializer(data=request.body)
            maria_host = request.data.get("maria_host", "")
            maria_user = request.data.get("maria_user", "")
            maria_pass = request.data.get("maria_pass", "")
            maria_db = request.data.get("maria_db", "")
            data = {
            }
            maria_conn = database.connect(
                user=maria_user,
                password=maria_pass,
                host=maria_host,
                database=maria_db)

            maria_file = pd.io.sql.read_sql('SHOW TABLES', maria_conn)
            maria_conn.close()
            collection_list = maria_file.iloc[:, 0].to_list()
            data['collection_list'] = json.dumps(collection_list)
        return JsonResponse(data)
 
# =============================================================================================================================

""" Retrieve Data from Mariadb"""

class mariadbSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mariadbSerializer
    
    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = mariadbSerializer(data=request.body)
            maria_host = request.data.get("maria_host", "")
            maria_user = request.data.get("maria_user", "")
            maria_db = request.data.get("maria_db", "")
            maria_table = request.data.get("maria_table", "")
            maria_pass = request.data.get("maria_pass", "")

            data = {
            }

            maria_conn = database.connect(
                user=maria_user,
                password=maria_pass,
                host=maria_host,
                database=maria_db)

            maria_file = pd.io.sql.read_sql('select * from '+maria_table, maria_conn)
            maria_conn.close()
            maria_json = maria_file.to_dict("records")

            res = len([ele for ele in maria_json if isinstance(ele, dict)])
            if str(res) == '0':
                content = {'response_msg': 'This table is Empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                data['file_data'] = json.dumps(maria_json)

                dtype_list = maria_file.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)

                file_name = 'mariadb_'+maria_table
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, maria_file)
                data['file_path'] = FileName

            return JsonResponse(data)