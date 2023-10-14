from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import SQLiteSerializer
from assets.global_state import PathAndRename
from assets.global_state import OverwriteStorage
from assets.global_state import downloadCsvFile
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import json, sqlite3, os, errno
import pandas as pd

# ViewSets define the view behavior.

""" Retrieve Collection List from SQLite DB """

class SQLite_TableSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = SQLiteSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == 'POST':
            data = {}
            try:
                sqlite_file = request.FILES.get('sqlite_file')
                if not sqlite_file:
                    Fileerror = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sqlite_file)
                    return JsonResponse({'File Not Found Error': str(Fileerror)}, status=status.HTTP_404_NOT_FOUND)   
                else:
                    fs = OverwriteStorage(location = 'media/')            
                    sqlite_path = fs.save(sqlite_file.name, sqlite_file)
                    url = 'media/'+sqlite_path
                    sqlite_conn = sqlite3.connect(url)
                    cursor = sqlite_conn.cursor()

                    sqlite_data = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", sqlite_conn)
                    sqlite_conn.close()
                    collection_list = sqlite_data['name'].to_list()
                    data['collection_list'] = json.dumps(collection_list)

            except pd.io.sql.DatabaseError  as err:
                return JsonResponse({'Database Error': str(err)}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Data from SQLite DB """

class SQLiteViewSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = SQLiteSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == 'POST':
            sqlite_file = request.FILES.get('sqlite_file')
            sqlite_table = request.POST.get("sqlite_table", "")

            fs = OverwriteStorage(location = 'media/')            
            sqlite_path = fs.save(sqlite_file.name, sqlite_file)
            url = 'media/'+sqlite_path

            data = {
            }

            sqlite_conn = sqlite3.connect(url)
            cursor = sqlite_conn.cursor()
            sqlite_data = pd.read_sql_query('SELECT * FROM '+sqlite_table, sqlite_conn)
            sqlite_json = sqlite_data.to_dict("records")
            sqlite_conn.close()

            res = len([ele for ele in sqlite_json if isinstance(ele, dict)])
            if str(res) == '0':
                content = {'response_msg': 'This table is Empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                data['file_data'] = json.dumps(sqlite_json)

                dtype_list = sqlite_data.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)

                file_name = 'SQLite3_'+sqlite_table 
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(file_name, sqlite_data)
                data['file_path'] = file_name
            return JsonResponse(data)
