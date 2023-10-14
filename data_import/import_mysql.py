from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import mysqlSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.global_state import DateTimeEncoder
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import json, pymysql
import pandas as pd
import numpy as np

# ViewSets define the view behavior.

""" Retrieve Database List from MySQL """

class mysql_ListSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mysqlSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = mysqlSerializer(data=request.body)
            mysql_host = request.data.get("mysql_host", "")
            mysql_user = request.data.get("mysql_user", "")
            mysql_pass = request.data.get("mysql_pass", "")

            data = {
            }
            try:
                mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass)
                cursor = mysql_conn.cursor()
                query = ("SHOW DATABASES")
                cursor.execute(query)

                mysql_file = pd.read_sql_query(query,mysql_conn)
                mysql_conn.close()
                database_list = mysql_file['Database'].to_list()
                data['database_list'] = json.dumps(database_list)
            except pymysql.Error as err:
                return JsonResponse({'Database Error': str(err)}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Table List from MySQL """

class mysql_TableSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mysqlSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = mysqlSerializer(data=request.body)
            mysql_host = request.data.get("mysql_host", "")
            mysql_user = request.data.get("mysql_user", "")
            mysql_pass = request.data.get("mysql_pass", "")
            mysql_db = request.data.get("mysql_db", "")

            data = {
            }
            mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass, database=mysql_db)
            cursor = mysql_conn.cursor()
            query = ("SHOW TABLES")
            cursor.execute(query)

            mysql_file = pd.read_sql_query(query,mysql_conn)
            mysql_conn.close()
            collection_list = mysql_file.iloc[:, 0].to_list()
            data['collection_list'] = json.dumps(collection_list)

            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Data from MySQL"""

class mysqlViewSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mysqlSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = mysqlSerializer(data=request.body)
            mysql_host = request.data.get("mysql_host", "")
            mysql_user = request.data.get("mysql_user", "")
            mysql_db = request.data.get("mysql_db", "")
            mysql_table = request.data.get("mysql_table", "")
            mysql_pass = request.data.get("mysql_pass", "")

            data = {
            }

            mysql_conn = pymysql.connect(host=mysql_host, database=mysql_db, user=mysql_user, passwd=mysql_pass)
            cursor = mysql_conn.cursor()
            query = ("SELECT * FROM "+mysql_table)
            cursor.execute(query)

            mysql_file = pd.read_sql_query(query,mysql_conn)
            mysql_json = mysql_file.to_dict("records")
            mysql_conn.close()

            res = len([ele for ele in mysql_json if isinstance(ele, dict)])
            if str(res) == '0':
                content = {'response_msg': 'This table is Empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                data['file_data'] = json.dumps(mysql_json, cls = DateTimeEncoder, indent = 4)

                dtype_list = mysql_file.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)
    
                file_name = 'MySQL_'+mysql_table
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, mysql_file)
                data['file_path'] = FileName
            return JsonResponse(data)