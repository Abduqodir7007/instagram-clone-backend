from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListView.as_view()),
    path("post/create/", PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view())
]
