from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from assets.serializers import UserSerializer
from assets.authentication import UserAuthentication
from assets.permission import UserAccessPermission

class UserRegistration(APIView):
    def post(self, request): 
        user_data = JSONParser().parse(request)
        try:
            user = User.objects.get(email=user_data['email'])
            print(user)
            user_serializer = UserSerializer(user) 
            return JsonResponse({'message': 'User email already exist!'}, status=status.HTTP_204_NO_CONTENT) 
        except User.DoesNotExist:
            user_serializer = UserSerializer(data=user_data)
            # if user_data['password']!=user_data['confirm_password']:
            #         return JsonResponse({'message': 'New and confirm password not match'}, status=status.HTTP_400_BAD_REQUEST)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    def get(self, request):
        user = User.objects.all()
        
        username = request.GET.get('username', None)
        if username is not None:
            user = user.filter(username__icontains=username)
        
        user_serializer = UserSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)
        # 'safe=False' for objects serialization
        
    def delete(self, request):
        count = User.objects.all().delete()
        return JsonResponse({'message': '{} User were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

class UserList(APIView): 
    authentication_classes = (UserAuthentication,)
    permission_classes = (UserAccessPermission,)

    def get(self, request, pk):
        try: 
            user = User.objects.get(pk=pk) 
            user_serializer = UserSerializer(user) 
            return JsonResponse(user_serializer.data) 
        except User.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)  
            
    
    def put(self, request, pk): 
        try: 
            user = User.objects.get(pk=pk) 
            user_data = JSONParser().parse(request) 
            user_serializer = UserSerializer(user, data=user_data, partial=True) 
            if user_serializer.is_valid(): 
                user_serializer.save() 
                return JsonResponse(user_serializer.data) 
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        except User.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
    
    def delete(self, request, pk): 
        try: 
            user = User.objects.get(pk=pk) 
            user.delete() 
            return JsonResponse({'message': 'user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)