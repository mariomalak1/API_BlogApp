import datetime
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import BlogSerializer
from .models import Blog
# Create your views here.

def valid_page_num_for_pagination(request, num_pages):
	page_number = request.GET.get("page", "")
	try:
		page_number = int(page_number)
	except ValueError:
		return 1
	if page_number > num_pages:
		page_number = num_pages
	elif page_number < 1:
		page_number = 1
	return page_number 

class BlogView(APIView):
	def post(self, request):
		data = request.data
		token = Token.objects.filter(key=data.get("token", "")).first()
		if token:
			# send user to data dict, to make serializer make it's validation
			mutable_data = request.data.copy()
			mutable_data["user"] = token.user.id
			data = mutable_data
			serializer = BlogSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_403_FORBIDDEN)

	def get(self, request):
		
		number_of_objects_per_page = request.GET.get("n_objects", 2)  
		search_query = request.GET.get("search", "")
		
		if search_query:
			blogs_objects = Blog.objects.filter(Q(title__icontains=search_query) | Q(user__username=search_query) | Q(blog_text__contains=search_query))
		else:
			blogs_objects = Blog.objects.all()
		
		blog_paginator = Paginator(blogs_objects, number_of_objects_per_page)

		# this function that take the request and return the valid page number
		page_number = valid_page_num_for_pagination(request, blog_paginator.num_pages)
		
		serializer = BlogSerializer(data=blog_paginator.page(page_number).object_list, many=True)
		if serializer.is_valid():
			serializer.data["number_of_pages"] = blog_paginator.num_pages
		
		return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "PATCH", "DELETE"])
def blog_detials(request):
	data = request.data
	token = Token.objects.filter(key=data.get("token", "")).first()
	
	blog_id = data.get("blog_id", 0)
	blog_ = get_object_or_404(Blog, id=blog_id)

	if token:
		if blog_.user.username == token.user.username:
			if request.method == "PATCH":
				serializer = BlogSerializer(data=data, instance=blog_, partial=True)
				# updated_data = serializer.partial_update(request)
				if serializer.is_valid():
					blog_.updated_at = datetime.datetime.now()
					serializer.save()
					return Response(serializer.data, status=status.HTTP_200_OK)
				else:
					return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		

			elif request.method == "DELETE":
				blog_.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)

		# any user with token can see the another blog or his blog 
		if request.method == "GET":
			serializer = BlogSerializer(instance=blog_)
			return Response(serializer.data, status=status.HTTP_200_OK)	

	return Response(status=status.HTTP_403_FORBIDDEN)


class Blog_Detials(APIView):
    def get(self, request, pk):
        blog_ = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog_)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk,format=None):
        blog = get_object_or_404(Blog, id=pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)