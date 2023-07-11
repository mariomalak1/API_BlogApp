from django.urls import path, include

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
]


# "token": "3e775af683522e2e46e483ebe10a086435ea33ca"