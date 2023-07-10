from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		exclude = ["create_at", "update_at", "id"]