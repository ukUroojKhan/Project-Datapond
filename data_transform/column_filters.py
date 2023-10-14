from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import ColumnFiltersSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import FileExtension
from assets.global_state import downloadCsvFile
from urllib.parse import urlparse
import os, ast, json
import pandas as pd

# ViewSets define the view behavior.
class ColumnFiltersViewSet(ViewSet):
    serializer_class = ColumnFiltersSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
    
        if request.method == "POST":
            serializer = ColumnFiltersSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            column_filter = request.POST.get("column_filter", "")

            print(column_filter, file_path)
            
            res = ast.literal_eval(column_filter)

            data = {
            }

            final_df = FileExtension().getuploadedfile(file_path, file_path)

            final_df = final_df[res]
            filtercols_to_json = final_df.to_dict("records")
            data['file_data'] = json.dumps(filtercols_to_json)

            a = urlparse(file_path)
            file_get = os.path.basename(a.path)
            downloadCsvFile().getdataframefile(file_get, final_df)
            
            return JsonResponse(data)