from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import SaveFileDBSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import con_mongodb
from assets.global_state import FileExtension
from assets.global_state import FileFormatting
import json, datetime, pymongo

# Package for accessing Mongo databases
from pymongo import MongoClient

class SaveFileDBViewSet(ViewSet):
    serializer_class = SaveFileDBSerializer

    def list(self, request): 
        return Response("GET API")

    def create(self, request):
        if request.method == "POST": 
            serializer = SaveFileDBSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))

            client =  MongoClient("mongodb://localhost:27017/")
            mongo_db = request.POST.get("user_email", "")
            mongo_collection =  request.POST.get("file_path", "")
            DataSettable = 'all_dataset'

            data = {
            }
 
            df = FileExtension().getuploadedfile(file_path, file_path)
            file_to_json = df.to_dict("records")
            data['file_data'] = json.dumps(file_to_json)

            db = client[mongo_db]
            collection = db[mongo_collection]
            dataset_collection = db[DataSettable]
            list_of_collections = db.list_collection_names()

            # Insert collection
            if mongo_collection in list_of_collections:
                collection.delete_many({})
                con_mongodb().getDataCursor(mongo_db, mongo_collection, file_to_json)
            else:
                con_mongodb().getDataCursor(mongo_db, mongo_collection, file_to_json)
            # Close collection

            # Collection for All DataSet
            created_at = datetime.datetime.now()
            file_size = fs.size(mongo_collection)
            file_format = FileFormatting().size_format(file_size)
            dataset_dic = [{'File_Name': mongo_collection ,'created_at': created_at, 'file_size': file_format }]
            
            # Insert collection for All DataSet
            if dataset_collection.count({ 'File_Name': mongo_collection }) == 0:  
                con_mongodb().getDataCursor(mongo_db, DataSettable, dataset_dic)
            else:
                myquery = { 'File_Name' : mongo_collection }
                newvalues = { "$set": { 'File_Name' : mongo_collection, 'created_at' : created_at} }
                collection.update_many(myquery, newvalues)
            # Close collection

        return JsonResponse(data)