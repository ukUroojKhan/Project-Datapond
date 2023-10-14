from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import firebaseSerializer
from assets.global_state import PathAndRename
from assets.global_state import downloadCsvFile
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission
import firebase_admin, json, os, errno
from firebase_admin import credentials, firestore
import pandas as pd

# ViewSets define the view behavior.
class FirebaseViewSet(ViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)
    
    serializer_class = firebaseSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            data = {}
            try:
                firebase_url = request.FILES.get("firebase_url", "")
                firebase_table = request.POST.get("firebase_table", "")
                firebase_cred = request.FILES.get('firebase_cred')

                if not firebase_cred:
                    Fileerror = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), firebase_cred)
                    return JsonResponse({'File Not Found Error': str(Fileerror)}, status=status.HTTP_404_NOT_FOUND)
                     
                else:
                    file_type = firebase_cred.content_type

                    if file_type == "application/json":
                        file_data = pd.read_json(firebase_cred, typ='series')
                        file_dic = file_data.to_dict()

                        if not firebase_admin._apps:
                            cred = credentials.Certificate(file_dic)
                            firebase_admin.initialize_app(cred, {'databaseURL': ''+firebase_url})
                            
                        db = firestore.client()
                        firebase_dict = []

                        for k in db.collection(firebase_table).get():
                            k = k.to_dict()
                            firebase_dict.append(k)

                        firebase_df = pd.DataFrame(firebase_dict)
                        firebase_json = firebase_df.to_dict("records")

                        # Dictionary Count in List
                        res = len([ele for ele in firebase_json if isinstance(ele, dict)])

                        if str(res) == '0':
                            content = {'response_msg': 'This table is empty.'}
                            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                        else: 
                            data['file_data'] = json.dumps(firebase_json)

                            dtype_list = firebase_df.dtypes.apply(lambda x: x.name).to_list()
                            data['dtype_list'] = json.dumps(dtype_list)

                            file_name = 'firebase_'+firebase_table
                            FileName = PathAndRename().name_call(file_name, 'csv')
                            downloadCsvFile().getdataframefile(FileName, firebase_df)
                            data['file_path'] = FileName
                    else:
                        content = {'response_msg': 'File Type Not Supported'}
                        return Response(content, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            except ValueError as verr:
                return JsonResponse({'Value Error': str(verr)}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(data)
