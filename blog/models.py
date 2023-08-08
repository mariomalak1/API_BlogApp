from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

# class BaseModel(models.Model):


class Blog(models.Model):
    def create_url(self, filename):
        print(filename)
        return "blogs/" + str(self.title) + "/main_images/" + str(filename)

    def update_filename(instance, filename):
        path = create_url(instance, filename)
        return os.path.join(path, instance.title)

    title = models.CharField(max_length=250, unique=True)
    user = models.ForeignKey(User, related_name="blogs", on_delete=models.CASCADE)
    blog_text = models.TextField()
    main_image = models.ImageField(upload_to=create_url)

    updated_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
