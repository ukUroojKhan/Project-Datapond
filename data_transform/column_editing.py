from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import ColumnEditSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import downloadCsvFile
from assets.global_state import FileExtension
from urllib.parse import urlparse
import ast, json, os


# ViewSets define the view behavior.
class ColumnEditViewSet(ViewSet):
    serializer_class = ColumnEditSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
    
        if request.method == "POST":
            serializer = ColumnEditSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            column_edit = request.POST.get("column_edit", "")
            res = ast.literal_eval(column_edit)            

            data = {
            }

            dataframe = FileExtension().getuploadedfile(file_path, file_path)
            dataframe.columns = res

            dataframe_to_json = dataframe.to_dict("records")
            data['file_data'] = json.dumps(dataframe_to_json)

            a = urlparse(file_path)
            file_get = os.path.basename(a.path)
            downloadCsvFile().getdataframefile(file_get, dataframe)
            data['file_path'] = file_get
            
            return JsonResponse(data)