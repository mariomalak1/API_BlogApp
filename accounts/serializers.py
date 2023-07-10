from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150)
	password = serializers.CharField(max_length=250)
	last_name = serializers.CharField(max_length=100, required=False)
	first_name = serializers.CharField(max_length=100, required=False)

	def validate_username(self, username):
		user = User.objects.filter(username=username).first()
		if user:
			raise serializers.ValidationError("this username is already taken")
		return username