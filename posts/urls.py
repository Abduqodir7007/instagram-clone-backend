from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListView.as_view()),
    path("create/", PostCreateView.as_view()),
    path("<uuid:pk>/", PostRetrieveUpdateDestroyView.as_view()),
    path("<uuid:pk>/like/", PostLikeCreateDeleteView.as_view()),
    path('<uuid:pk>/comments/', PostCommentList.as_view()),  
    path("<uuid:pk>/comment/create/", PostCommentCreateView.as_view()),
    
    path("comments/", CommentCreateView.as_view())
    
    
]
