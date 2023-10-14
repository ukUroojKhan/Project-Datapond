from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import postgresSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.global_state import DateTimeEncoder
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import json, psycopg2 
import numpy as np
import pandas as pd

# ViewSets define the view behavior.

""" Retrieve Table List from PostGreSQL """

class postgres_TableSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = postgresSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = postgresSerializer(data=request.body)
            psql_host = request.data.get("psql_host", "")
            psql_user = request.data.get("psql_user", "")
            psql_pass = request.data.get("psql_pass", "")
            psql_db = request.data.get("psql_db", "")
            data = {
            }
            try:
                conn_string = "host={} dbname={} user={} password={}".format(psql_host, psql_db, psql_user, psql_pass)
                with psycopg2.connect(conn_string) as connection:
                    with connection.cursor() as cursor:
                        def create_pandas_table(sql_query, database = connection):
                            table = pd.read_sql_query(sql_query, database)
                            return table
                        psql_file = create_pandas_table("SELECT * FROM INFORMATION_SCHEMA.TABLES;")
                collection_list = psql_file['table_name'].to_list()
                data['collection_list'] = json.dumps(collection_list)
            except psycopg2.Error as err:
                return JsonResponse({'Database Error': str(err)}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Data from PostGreSQL """

class postgresSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = postgresSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = postgresSerializer(data=request.body)
            psql_host = request.data.get("psql_host", "")
            psql_user = request.data.get("psql_user", "")
            psql_db = request.data.get("psql_db", "")
            psql_table = request.data.get("psql_table", "")
            psql_pass = request.data.get("psql_pass", "")
            
            data = {
            }

            conn_string = "host={} dbname={} user={} password={}".format(psql_host, psql_db, psql_user, psql_pass)
            with psycopg2.connect(conn_string) as connection:
                with connection.cursor() as cursor:
                    def create_pandas_table(sql_query, database = connection):
                        table = pd.read_sql_query(sql_query, database)
                        return table
                    psql_file = create_pandas_table("SELECT * FROM "+psql_table)
            psql_json = psql_file.to_dict("records")

            res = len([ele for ele in psql_json if isinstance(ele, dict)])
            if str(res) == '0':
                content = {'response_msg': 'This File is Empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)   
                
            else:
                data['file_data'] = json.dumps(psql_json, cls = DateTimeEncoder, indent = 4)

                dtype_list = psql_file.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)

                file_name = 'postgre_'+psql_table
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, psql_file)
                data['file_path'] = FileName

        return JsonResponse(data)