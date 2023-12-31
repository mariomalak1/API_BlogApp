from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def get(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            token_dict = serializer.create_token(serializer.data, request)
            return Response(token_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def register(request):
# 	if request.method == "POST":
# 		data = request.data
# 		serializer = RegisterSerializer(data=data)
# 		if serializer.is_valid():
# 			serializer.create(serializer.data)
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		else:
# 			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def login(request):
# 	data = request.data
# 	serializer = LoginSerializer(data=data)
# 	if serializer.is_valid():
# 		user = authenticate(username=serializer.data.get("username"), password=serializer.data.get("password"))
# 		django_login(request, user=user)

# 		token = Token.objects.filter(user=user).first()
# 		if not token:
# 			token = Token.objects.create(user = user)
# 		return Response({"token": str(token)}, status=status.HTTP_200_OK)
# 	else:
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
