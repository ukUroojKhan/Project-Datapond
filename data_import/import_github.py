from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import (
    gitprivateSerializer, 
    gitpublicSerializer, )
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
from urllib.parse import urlparse
import requests, json, io, os
import pandas as pd


# ViewSets define the view behavior.
class gitprivateSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    serializer_class = gitprivateSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = gitprivateSerializer(data=request.data)
            git_username = request.data.get("git_username", "")
            git_token = request.data.get("git_token", "")
            git_url = request.data.get("git_url", "")

            data = {
            }

            a = urlparse(git_url)
            file_get = os.path.basename(a.path)
            file_name = 'git_'+file_get

            github_session = requests.Session()
            github_session.auth = (git_username, git_token)
            download = github_session.get(git_url).content

            git_pvtdf = pd.read_csv(io.StringIO(download.decode('utf-8')))
            git_json = git_pvtdf.to_dict("records")

            # Dictionary Count in List
            res = len([ele for ele in git_json if isinstance(ele, dict)])

            if str(res) == '0':
                content = {'response_msg': 'This table is empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            else: 
                data['file_data'] = json.dumps(git_json)

                dtype_list = git_pvtdf.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)

                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, git_pvtdf)
                data['file_path'] = FileName

        return JsonResponse(data, status=status.HTTP_200_OK)

class gitpublicSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)
    
    serializer_class = gitpublicSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        if request.method == "POST":
            serializer = gitpublicSerializer(data=request.data)
            git_puburl = request.data.get("git_puburl", "")

            data = {
            }

            a = urlparse(git_puburl)
            file_get = os.path.basename(a.path)
            
            git_pubdf = (pd.read_csv(git_puburl, index_col=0)).reset_index()
            git_json = git_pubdf.to_dict("records")

            res = len([ele for ele in git_json if isinstance(ele, dict)])
            if str(res) == '0':
                content = {'response_msg': 'This table is empty.'}
                return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                data['file_data'] = json.dumps(git_json)

                dtype_list = git_pubdf.dtypes.apply(lambda x: x.name).to_list()
                data['dtype_list'] = json.dumps(dtype_list)

                file_name = 'git_'+file_get
                FileName = PathAndRename().name_call(file_name, 'csv')
                downloadCsvFile().getdataframefile(FileName, git_pubdf) 
                data['file_path'] = FileName

        return JsonResponse(data, status=status.HTTP_200_OK)