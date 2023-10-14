from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.core import mail

class ForgetPassword(APIView):
    
     def post(self, request):
            user_data = JSONParser().parse(request)
            try:
                user = User.objects.get(email=user_data['email'])
                # user_serializer = UserSerializer(user)
                msg = EmailMessage('Request Callback',
                       'Here is the message.', to=[user_data['email']])
                msg.send()
                return JsonResponse({'message': 'Email has been send'}, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return JsonResponse({'message': 'User email does not exist!'}, status=status.HTTP_204_NO_CONTENT)