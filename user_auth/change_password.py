from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission

class ChangePassword(APIView): 
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)
        
    def put(self, request, pk): 
        
        try: 
            user_data = JSONParser().parse(request) 
            u = User.objects.get(id__exact=pk)
            cur=u.check_password(user_data['current'])
           
            if cur==True: 
                if user_data['new']==user_data['confirm']:
                    u = User.objects.get(id__exact=pk)
                    u.set_password(user_data['confirm'])
                    u.save()
                    return JsonResponse({'message': 'Password changed Successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'message': 'New and confirm password not match'}, status=status.HTTP_400_BAD_REQUEST)
            else:       
                return JsonResponse({'message': 'Current password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)