from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import BlogSerializer
# Create your views here.

class BlogView(APIView):
	def post(self, request):
		data = request.data
		token = Token.objects.filter(key=data.get("token", "")).first()
		if token:
			# send user to data dict, to make serializer make it's validation
			data["user"] = token.user.id
			serializer = BlogSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				print("serializer user:", serializer.data.get("user"))
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_404_NOT_FOUND)

# 