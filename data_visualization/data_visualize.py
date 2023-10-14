from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import visualizeSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import FileExtension
import pandas as pd, json, random

# ViewSets define the view behavior.
class VisualizeViewSet(ViewSet):
    serializer_class = visualizeSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = visualizeSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            visualize_col1 = request.POST.get("visualize_col1", "")
            visualize_col2= request.POST.get("visualize_col2", "")

            data = {
            }

            df = FileExtension().getuploadedfile(file_path, file_path)

            lst1 = []
            for x in df[visualize_col1]:
                lst1.append(x)

            colr_lst = []
            for y in range(len(df[visualize_col1])):
                rand_colors = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
                colr_lst.append(rand_colors)

            lst2 = []
            for z in df[visualize_col2]:
                lst2.append(z)

            data = {
                'value_1' : json.dumps(lst1),
                'value_2' : json.dumps(lst2),
                'colr_lst' : json.dumps(colr_lst)
            }

            return JsonResponse(data)

            # data = {
            #     'value_1' : lst1,
            #     'value_2' : lst2,
            #     'colr_lst' : colr_lst
            # }

            # return JsonResponse(json.dumps(data), safe = False)