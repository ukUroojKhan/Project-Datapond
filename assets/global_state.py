from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from assets.serializers import clientSerializer
import json, csv, openpyxl, os, uuid
import pandas as pd, numpy as np
import json, datetime
from json import JSONEncoder

# Package for accessing Mongo databases
from pymongo import MongoClient

class clientViewSet(ViewSet):
    serializer_class = clientSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST": 
            serializer = clientSerializer(data=request.data)
            email = request.data.get("useremail", "")
            client_email = email.replace(".","_")
            data = {}
            data["user_email"] = client_email
            return JsonResponse(data)

class PathAndRename:
    def name_call(self, filename, ext):
        #eg: 'Sample.csv'
        extt = filename.split('.')[-1]  #eg: '.csv'
        uid = uuid.uuid4().hex[:3] #eg: '567ae32f97'
        new_name = '_'.join(filename.replace('.%s' % extt, '').split()) #eg: 'Sample'
        renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}
        return renamed_filename

class downloadCsvFile:
    def getdataframefile(self, csvFile, DataFrame):
        path = 'media/'
        output_file = os.path.join(path, csvFile)
        DataFrame.to_csv(output_file, index=False)
        return output_file

class con_mongodb:
    def getDataCursor(self, user_db, table_name, file_document):
        client =  MongoClient("mongodb://localhost:27017/")
        db = client[user_db]
        collection = db[table_name]
        insert_table = collection.insert_many(file_document)
        return insert_table

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length = None):
        if self.exists(name):
            os.remove(os.path.join('media/', name))
        return name

class txtUpload:
    def gettxtfile(self, upload_txtfile):
        txt_data = np.loadtxt(upload_txtfile, delimiter=',', dtype=str)
        txt_df = (pd.DataFrame(txt_data)).T
        txt_dict = txt_df.set_index(0).T.to_dict('list')
        dict_txtfile = pd.DataFrame(txt_dict)
        return dict_txtfile

class csvUpload:
    def getcsvfile(self, upload_csvfile):
        dict_csvfile = pd.read_csv(upload_csvfile, encoding='latin-1')
        return dict_csvfile

class tsvUpload:
    def gettsvfile(self, upload_tsvfile):
        dict_tsvfile = pd.read_csv(upload_tsvfile, delimiter='\t')
        return dict_tsvfile

class jsonUpload:
    def getjsonfile(self, upload_jsonfile):
        json_data = pd.read_json(upload_jsonfile, typ='series')
        dict_jsonfile= (pd.DataFrame(json_data)).T
        return dict_jsonfile

class excelUpload:
    def getexcelfile(self, upload_excelfile):
        dict_excelfile = pd.read_excel(upload_excelfile, engine='openpyxl')
        return dict_excelfile

class FileExtension:
    def getuploadedfile(self, file_ext, fileRead):
        if file_ext.endswith('.txt'):
            df = txtUpload().gettxtfile(fileRead)
        elif file_ext.endswith('.csv'):
            df = csvUpload().getcsvfile(fileRead)
        elif file_ext.endswith('.tsv'):
            df = tsvUpload().gettsvfile(fileRead) 
        elif file_ext.endswith('.json'):
            df = jsonUpload().getjsonfile(fileRead)
        elif file_ext.endswith('.xlsx') or file_ext.endswith('.xls'):
            df = excelUpload().getexcelfile(fileRead)
        return df

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

class ChunksData:
    def split_dataframe(self, df, chunk_size = 200): 
        chunks = list()
        num_chunks = len(df) // chunk_size + 1
        for i in range(num_chunks):
            chunks.append(df[i*chunk_size:(i+1)*chunk_size])
        return chunks

class FileFormatting:
    def size_format(self, b):
        if b < 1024:
            FS = str(b) + 'B'
        elif 1024 <= b < 1000000:
            FS =str(int(b/1000)) + 'KB'
        elif 1000000 <= b < 1000000000:
            FS = str(int(b/1000000)) + 'MB'
        elif 1000000000 <= b < 1000000000000:
            FS = str(int(b/1000000000)) + 'GB'
        elif 1000000000000 <= b:
            FS = str(int(b/1000000000000)) + 'TB'
        return FS