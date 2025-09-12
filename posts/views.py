from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import *
from .models import *
from posts.custom_pagination import CustomPagination


class PostCreateView(CreateAPIView):
    serializer_class = PostSerilalizer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class PostListView(ListAPIView):
    serializer_class = PostSerilalizer
    queryset = Post.objects.all()

    pagination_class = CustomPagination


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = PostSerilalizer
    queryset = Post.objects.all()
    lookup_field = "pk"
