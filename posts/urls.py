from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListView.as_view()),
    path("create/", PostCreateView.as_view()),
    path("<uuid:pk>/", PostRetrieveUpdateDestroyView.as_view()),
    path("<uuid:pk>/comments/", PostCommentList.as_view()), 
    path("<uuid:pk>/comment/create/", PostCommentCreateView.as_view()),
    path("<uuid:pk>/likes/", PostLikesView.as_view()),
    path("<uuid:pk>/create-delete-like/", PostLikeCreateDeleteView.as_view()),
    
    path("comments/", CommentListView.as_view()), 
    path("comment/create/", CommentCreateView.as_view()),
    path("comment/<uuid:pk>/likes/", CommentLikeListView.as_view()),
    path("comment/<uuid:pk>/create-delete-like/", CommentLikeView.as_view()),
    
]
