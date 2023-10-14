from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import UploadSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.global_state import FileExtension
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
from urllib.parse import urlparse
import json, os, errno


# ViewSets define the view behavior.

""" Retrieve Data from File (.xls, .csv, .tsv, .txt, .json) """

class UploadViewSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            data = {}
            try: 
                upload_file = request.FILES.get('file_uploaded')
                if not upload_file:
                    Fileerror = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), upload_file)
                    return JsonResponse({'File Not Found Error': str(Fileerror)}, status=status.HTTP_404_NOT_FOUND)   
                else:
                    file_name = upload_file.name
                    file_type = upload_file.content_type

                    if file_type == "text/tab-separated-values" \
                    or file_type == "text/plain" \
                    or file_type == "application/vnd.ms-excel" \
                    or file_type == "text/csv" \
                    or file_type == "application/json" \
                    or file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
    
                        df = FileExtension().getuploadedfile(file_name, upload_file)
                        file_to_json = df.to_dict("records")
                        
                        res = len([ele for ele in file_to_json if isinstance(ele, dict)])
                        if str(res) == '0':
                            content = {'response_msg': 'This File is Empty.'}
                            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)   
                        else: 
                            data['file_data'] = json.dumps(file_to_json)

                            dtype_list = df.dtypes.apply(lambda x: x.name).to_list()
                            data['dtype_list'] = json.dumps(dtype_list)

                            data['file_type'] = file_type

                            FileName = PathAndRename().name_call(file_name, 'csv')
                            downloadCsvFile().getdataframefile(FileName, df)
                            data['file_path'] = FileName
                            return JsonResponse(data)
                    else:
                        content = {'response_msg': 'File Type Not Supported'}
                        return Response(content, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            except:
                return JsonResponse(data)

# ======================================================================================================