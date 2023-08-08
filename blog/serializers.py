from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(required=True, max_length=250)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        if self.partial:
            for field in self.fields.values():
                field.required = False
        return super().is_valid(raise_exception=raise_exception)

    # def validate_title(self, value):
    # 	if Blog.objects.filter(title=value).exists():
    # 		raise serializers.ValidationError('Title must be unique')
    # 	return value

    # def partial_update(self, request, *args, **kwargs):
    # 	instance_object = self.instance

    # 	if not instance_object:
    # 		if self.is_valid():
    # 			return self.data
    # 		else:
    # 			return self.errors
    # 	else:
    # 		mutable_data = request.data.copy()
    # 		if not mutable_data.get("title"):
    # 			mutable_data["title"] = instance_object.title
    # 		else:
    # 			instance_object.title = mutable_data["title"]
    # 		if not mutable_data.get("blog_text"):
    # 			mutable_data["blog_text"] = instance_object.blog_text
    # 		else:
    # 			instance_object.blog_text = mutable_data["blog_text"]
    # 		if not mutable_data.get("main_image"):
    # 			mutable_data["main_image"] = instance_object.main_image
    # 		else:
    # 			instance_object.main_image = mutable_data["main_image"]

    # 		data = mutable_data

    # 		if self.validate(data):
    # 			self.is_valid()
    # 			instance_object.save()
    # 			return self.data
    # 		else:
    # 			self.is_valid()
    # 			return self.errors
