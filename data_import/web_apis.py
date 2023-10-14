from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import ApisSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
import json, requests
import pandas as pd

# ViewSets define the view behavior.
class ApisViewSet(ViewSet):
    serializer_class = ApisSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = ApisSerializer(data=request.data)
            apis_url = request.data.get("apis_url", "")

            data = {
            }

            file_name = 'API FILE'

            response = requests.get(apis_url)
            apis_data = response.text
            apis_parsed = json.loads(apis_data)
            apis_df = pd.DataFrame(apis_parsed)
            apis_set_index = apis_df.insert(0,'column', apis_df.index, True)
            apis_df.reset_index(drop=True,inplace=True)
            apis_json = apis_df.to_dict("records")
            data['file_data'] = json.dumps(apis_json)

            FileName = PathAndRename().name_call(file_name, 'csv')
            downloadCsvFile().getdataframefile(FileName, apis_df)
            data['file_path'] = FileName

        else:
            data['response_code'] = "415"
            data['response_msg'] = "UNSUPPORTED_FILE_TYPE"

        return JsonResponse(data, status=status.HTTP_200_OK)