from django.urls import path
from . import views

urlpatterns = [
    path("blogs/", views.BlogView.as_view(), name="blogs"),
    path("blog_detials/", views.blog_detials, name="blog_detail"),
    path("user_blogs/", views.user_blogs, name="user_blogs"),
]
