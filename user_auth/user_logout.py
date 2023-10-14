from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user_auth.models import Session
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission

class Logout(APIView):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)
       
    def delete(self, request): 
        auth_token = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
    
        try: 
            session = Session.objects.get(token=auth_token) 
            session.delete()
            return JsonResponse({'message': 'Logout successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist: 
            return JsonResponse({'message': 'Token does not exist'}, status=status.HTTP_404_NOT_FOUND)