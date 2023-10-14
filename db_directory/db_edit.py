from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.global_state import downloadCsvFile
from assets.global_state import DateTimeEncoder
import pandas as pd
import json, pymongo

# Package for accessing Mongo databases
from pymongo import MongoClient

class EditDBViewSet(ViewSet):

    def list(self, request): 
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            client =  MongoClient("mongodb://localhost:27017/")
            mongo_db = request.POST.get("user_email", "")
            mongo_collection =  request.POST.get("File_Name", "")

            data = {
            }
 
            mydb = client[mongo_db]
            mycol = mydb[mongo_collection]

            mongo_dic = []
            for xmongo in mycol.find():
                mongo_dic.append(xmongo)
            
            mongo_file =  pd.DataFrame(list(mongo_dic))
            mongo_df = mongo_file.drop(['_id'],axis='columns')
            mongo_json = mongo_df.to_dict("records")
            data['file_data'] = json.dumps(mongo_json, cls = DateTimeEncoder, indent = 4)

            dtype_list = mongo_df.dtypes.apply(lambda x: x.name).to_list()
            data['dtype_list'] = json.dumps(dtype_list)

            downloadCsvFile().getdataframefile(mongo_collection, mongo_df)
            data['file_path'] = mongo_collection

        return JsonResponse(data)