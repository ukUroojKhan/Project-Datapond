from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import mongodbSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.global_state import DateTimeEncoder
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import json, pymongo
from pymongo import MongoClient
import pandas as pd

# ViewSets define the view behavior.

""" Retrieve Database List from Mongodb """

class mongodb_ListSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mongodbSerializer

    def list(self, request):
        return Response("GET API")
    def create(self, request):
        if request.method == "POST":
            serializer = mongodbSerializer(data=request.body)
            mongo_client = request.data.get("mongo_client", "")
            data = {
            }
            try:
                if not mongo_client:
                    Configerr = pymongo.errors.ConfigurationError("Empty host (or extra comma in host list)")
                    return JsonResponse({'Configuration Error': str(Configerr)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        maxSevSelDelay = 2000
                        myclient = pymongo.MongoClient(mongo_client, serverSelectionTimeoutMS=maxSevSelDelay)
                    except pymongo.errors.InvalidURI as URIerr:
                        return JsonResponse({'Invalid Mongodb URI': str(URIerr)}, status=status.HTTP_401_UNAUTHORIZED)
                    myclient.server_info()
                    database_list = myclient.list_database_names()
                    data['database_list'] = json.dumps(database_list)
            except pymongo.errors.ServerSelectionTimeoutError as SSLerr:
                return JsonResponse({'Server Selection Error': str(SSLerr)}, status=status.HTTP_408_REQUEST_TIMEOUT)
            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Collection List from Mongodb """

class mongodb_CollectionSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mongodbSerializer
    def list(self, request):
        return Response("GET API")
    def create(self, request):
        if request.method == "POST":
            serializer = mongodbSerializer(data=request.body)
            mongo_client = request.data.get("mongo_client", "")
            mongo_db = request.data.get("mongo_db", "")
            data = {
            }
            myclient = pymongo.MongoClient(mongo_client)
            mydb = myclient[mongo_db]
            collection_list = mydb.list_collection_names()
            data['collection_list'] = json.dumps(collection_list)  

            return JsonResponse(data)

# =============================================================================================================================

""" Retrieve Documents from Mongodb"""

# ViewSets define the view behavior.
class mongodbSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = mongodbSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = mongodbSerializer(data=request.body)
            mongo_client = request.data.get("mongo_client", "")
            mongo_db = request.data.get("mongo_db", "")
            mongo_collection = request.data.get("mongo_collection", "")

            data = {
            }

            myclient = pymongo.MongoClient(mongo_client)
            mydb = myclient[mongo_db]
            mycol = mydb[mongo_collection]

            mongo_dic = []
            for xmongo in mycol.find():
                mongo_dic.append(xmongo)
            
            if len(mongo_dic) == 0:
                content = {'response_msg': "This table is Empty."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                mongo_file =  pd.DataFrame(list(mongo_dic))
                mongo_df = mongo_file.drop(['_id'],axis='columns')
                mongo_json = mongo_df.to_dict("records")
                data['file_data'] = json.dumps(mongo_json, cls = DateTimeEncoder, indent = 4)

                dtype_list = mongo_file.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)

                file_name = 'mongodb_'+mongo_collection
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, mongo_df)
                data['file_path'] = FileName

            return JsonResponse(data)

