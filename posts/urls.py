from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListView.as_view()),
    path("<uuid:pk>/", PostRetrieveUpdateDestroyView.as_view()),
    path("create/", PostCreateView.as_view()),
    path("<uuid:pk>/comment/create/", PostCommentCreateView.as_view()), #  create comment for a post
    path('<uuid:pk>/comments/', PostCommentList.as_view()), # list of comments 
    
    
    path("<uuid:pk>/like/", PostLikeView.as_view()),
   # path('post/')
    
]
