from django.urls import path
from .views import *

urlpatterns = [
    path("post/create/", PostCreateView.as_view()),
    path("", PostListView.as_view()),
]
