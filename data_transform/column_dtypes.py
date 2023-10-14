from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import DatatypeSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import FileExtension
import pandas as pd
import json


'''
happiness_2015['Happiness Rank'] = happiness_2015['Happiness Rank'].astype(str)
'''

class ColumnsdtypeViewSet(ViewSet):
    serializer_class = DatatypeSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
    
        if request.method == "POST":
            serializer = DatatypeSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            data_type = request.POST.get("data_type", "")
            selected_column = request.POST.get("selected_column", "")
            
            data = {
            }

            df = FileExtension().getuploadedfile(file_path, file_path)

            if df[selected_column].dtype == "O":
                if data_type == "int32" or data_type == "int64":
                    # data['response_msg'] = ''
                    content = {'response_msg': "We can't automatically convert the column to int() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                elif data_type == "float32" or data_type == "float64":
                    content = {'response_msg': "We can't automatically convert the column float() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                elif data_type == "bool":
                    content = {'response_msg': "We can't automatically convert the column bool() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                elif data_type == "datetime":
                    content = {'response_msg': "We can't automatically convert the column datetime() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                elif data_type == "complex":
                    content = {'response_msg': "We can't automatically convert the column complex() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                else:
                    df[selected_column] = df[selected_column].astype(data_type)
                    content = {'response_msg': 'Successfully changed'}
                    return Response(content, status=status.HTTP_205_RESET_CONTENT)
                    

            elif df[selected_column].dtype == "int64" or df[selected_column].dtype == "int32":
                if data_type == "bool":
                    content = {'response_msg': "We can't automatically convert the column bool() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                elif data_type == "datetime":
                    content = {'response_msg': "We can't automatically convert the column datetime() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                elif data_type == "complex":
                    content = {'response_msg': "We can't automatically convert the column complex() Type"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                else:
                    # data['response_msg'] = "Successfully changed"
                    df[selected_column] = df[selected_column].astype(data_type)
                    content = {'response_msg': 'Successfully changed'}
                    return Response(content, status=status.HTTP_205_RESET_CONTENT)
            else:
                df[selected_column] = df[selected_column].astype(data_type)

            print()

            filtercols_to_json = df.to_dict("records")
            data['file_data'] = json.dumps(filtercols_to_json)
            
            return JsonResponse(data)