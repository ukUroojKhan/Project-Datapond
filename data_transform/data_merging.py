from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import MergeUploadSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import downloadCsvFile
from assets.global_state import FileExtension
from urllib.parse import urlparse
import pandas as pd
import json, os



'''
merged = pd.merge(df1, df2, on = [left_on_col, right_on_col], how = how, 
left_index = True, right_index = True, suffixes = (suffixes_x, suffixes_y))
'''

class mergingViewSet(ViewSet):
    serializer_class = MergeUploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = MergeUploadSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            file_path1 = fs.path(request.POST.get("file_path1", ""))
            left_on_col = request.POST.get('left_on_col', '')
            right_on_col = request.POST.get('right_on_col', '')
            how = request.POST.get('how', '')
            suffixes_x = request.POST.get('suffixes_x', '')
            suffixes_y = request.POST.get('suffixes_y', '')
            
            data = {
            }

            df1 = FileExtension().getuploadedfile(file_path, file_path)
            df2 = FileExtension().getuploadedfile(file_path1, file_path1)

            

            if suffixes_x == "" or suffixes_y == "":
                merged_data = pd.merge(
                df1, df2, 
                on = [left_on_col, right_on_col], 
                how = how,
                left_index = True, right_index = True
            )
            else:
                merged_data = pd.merge(
                    df1, df2, 
                    on = [left_on_col, right_on_col], 
                    how = how,
                    suffixes = (suffixes_x,suffixes_y),
                    left_index = True, right_index = True
                )

            merge_to_json = merged_data.to_dict("records")
            data['file_data'] = json.dumps(merge_to_json)

            dtype_list = merged_data.dtypes.apply(lambda x: x.name).to_list()
            data['dtype_list'] = json.dumps(dtype_list)

            a = urlparse(file_path)
            file_get = os.path.basename(a.path)
            downloadCsvFile().getdataframefile(file_get, merged_data)

            return JsonResponse(data)
