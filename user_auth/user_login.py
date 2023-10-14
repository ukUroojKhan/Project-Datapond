from django.shortcuts import render
from django.contrib.auth.models import User,update_last_login
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from assets.serializers import UserLoginSerializer, SessionSerializer
from django.contrib.sessions.models import Session

class LoginView(APIView):
    
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            serializer = UserLoginSerializer(authenticated_user)
            data = {
                'user_id': serializer.data['id'],
                'token': serializer.data['token'],
            } 
            Session_serializer = SessionSerializer(data=data)
            if Session_serializer.is_valid():
                user = User.objects.get(id__exact=serializer.data['id'])
                update_last_login(None, user)
                Session_serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED) 