from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .serializers import RegisterSerializer
# Create your views here.


@api_view(["POST"])
def register(request):
	if request.method == "POST":
		data = request.data
		serializer = RegisterSerializer(data=data)
		if serializer.is_valid():
			new_user = User.objects.create(username=serializer.data.get("username"))
			new_user.set_password(serializer.data.get("password"))
			if serializer.data.get("last_name"):
				new_user.last_name = serializer.data.get("last_name")
			if serializer.data.get("first_name"):
				new_user.first_name = serializer.data.get("first_name")
			new_user.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

