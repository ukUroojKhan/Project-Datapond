from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.global_state import DateTimeEncoder
import json, pymongo
import pandas as pd

# Package for accessing Mongo databases
from pymongo import MongoClient

class AllDataSetViewSet(ViewSet):
    
    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            client =  MongoClient("mongodb://localhost:27017/")
            mongo_db = request.POST.get("user_email", "")
            DataSettable = 'all_dataset'
            
            data = {
            }

            db = client[mongo_db]
            dataset_collection = db[DataSettable]

            # This is a cursor instance
            cur = dataset_collection.find()   
            results = list(cur)

            if len(results) == 0:
                data['response_code'] = "003"
                data['response_msg'] = "Empty DataSet"

            else:
                mongo_dic = []
                for xmongo in dataset_collection.find():
                    mongo_dic.append(xmongo)
                
                mongo_file =  pd.DataFrame(list(mongo_dic))
                desc_file = mongo_file.sort_values(['created_at'], ascending=False)
                mongo_df = desc_file.drop(['_id'],axis='columns')
                mongo_json = mongo_df.to_dict("records")
                data['All_DataSet'] = json.dumps(mongo_json, cls = DateTimeEncoder, indent = 4)

        return JsonResponse(data)