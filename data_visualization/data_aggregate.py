from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from assets.serializers import aggregateSerializer
from assets.global_state import OverwriteStorage
from assets.global_state import FileExtension

import pandas as pd
import json

class aggregateViewSet(ViewSet):
    serializer_class = aggregateSerializer
    
    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method == "POST":
            serializer = aggregateSerializer(data=request.data)
            fs = OverwriteStorage(location = 'media/')
            file_path = fs.path(request.POST.get("file_path", ""))
            # agg_file = request.FILES.get('agg_file')
            agg_col = request.POST.get('agg_col', '')
            agg_value = request.POST.get('agg_value', '')

            data = {
            }

            # data['file_type'] = agg_file.content_type
            # file_name = agg_file.name
            aggr_df = FileExtension().getuploadedfile(file_path, file_path)

            if aggr_df[agg_col].dtype == "O" or aggr_df[agg_col].dtype == '<M8[ns]':
                if agg_value == 'first':
                    agg_return =  aggr_df[agg_col].iloc[0]
                if agg_value == 'last':
                    agg_return =  aggr_df[agg_col].iloc[-1]
                if agg_value == 'count':
                    agg_return =  len(aggr_df[agg_col]) 

            else:
                if agg_value == 'sum':
                    agg_return = aggr_df[agg_col].sum()
                elif agg_value == 'count':
                    agg_return = aggr_df[agg_col].count()
                elif agg_value == 'min':
                    agg_return = aggr_df[agg_col].min()
                elif agg_value == 'max':
                    agg_return = aggr_df[agg_col].max()
                elif agg_value == 'mean':
                    agg_return = aggr_df[agg_col].mean()
                elif agg_value == 'std':
                    agg_return = aggr_df[agg_col].std()
                elif agg_value == 'var':
                    agg_return = aggr_df[agg_col].var()        

            str_conv = str(agg_return)
            data['aggregate_data'] = str_conv

            return JsonResponse(data)