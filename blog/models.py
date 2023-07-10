from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class BaseModel(models.Model):



class Blog(models.Model):
	title = models.CharField(max_length=250)
	user = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
	blog_text = models.TextField()
	main_image = models.ImageField()
	
	updated_at = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)