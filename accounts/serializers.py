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

	def create(self, validated_data):
		new_user = User.objects.create(username=validated_data.get("username"))
		new_user.set_password(validated_data.get("password"))
		if validated_data.get("last_name"):
			new_user.last_name = validated_data.get("last_name")
		if validated_data.get("first_name"):
			new_user.first_name = validated_data.get("first_name")
		new_user.save()

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150)
	password = serializers.CharField(max_length=150)


	def validate(self, data):
		user = User.objects.filter(username=data.get("username")).first()
		if not user:
			raise serializers.ValidationError("Username Not Found")
		return data 

	