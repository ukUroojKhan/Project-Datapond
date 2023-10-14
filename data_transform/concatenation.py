from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import ConcatUploadSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import downloadCsvFile
from assets.global_state import FileExtension
from urllib.parse import urlparse
import json, os
import pandas as pd

'''
concatenate = pd.concat([df1,df2], axis : {0/'index', 1/'columns'}, ignore_index = True)
'''

class concatViewSet(ViewSet):
    serializer_class = ConcatUploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = ConcatUploadSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            file_uploaded2 = request.FILES.get('file_uploaded2')
            axis = request.POST.get('axis', '')

            data = {
            }

            file_name = file_uploaded2.name
            data['file_type'] = file_uploaded2.content_type

            df1 = FileExtension().getuploadedfile(file_path, file_path)
            df2 = FileExtension().getuploadedfile(file_name, file_uploaded2)
            
            concat_data = pd.concat(
                [df1,df2],
                axis = axis,
                ignore_index = True 
            )

            concat_to_json = concat_data.to_dict("records")
            data['file_data'] = json.dumps(concat_to_json)

            dtype_list = concat_data.dtypes.apply(lambda x: x.name).to_list()
            data['dtype_list'] = json.dumps(dtype_list)

            a = urlparse(file_path)
            file_get = os.path.basename(a.path)
            downloadCsvFile().getdataframefile(file_get, concat_data)

            return JsonResponse(data)