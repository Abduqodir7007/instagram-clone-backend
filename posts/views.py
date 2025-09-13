from .models import *
from posts.permissions import IsOwner
from posts.custom_pagination import CustomPagination
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.utils import IntegrityError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)


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
    permission_classes = [IsOwner]
    serializer_class = PostSerilalizer
    queryset = Post.objects.all()
    lookup_field = "pk"


class PostCommentCreateView(APIView):

    def post(self, request, pk):
        user = request.user
        post = Post.objects.get(id=pk)
        serializer = PostCommentViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PostComment.objects.create(
            author=user, post=post, comment=serializer.validated_data.get("comment")
        )
        return Response({"msg": "comment created"})

    # queryset = PostComment.objects.all()
    # serializer_class = PostCommentViewSerializer

    # def perform_create(self, serializer):
    #     print(self.request)
    #     post = Post.objects.get(id=self.request)
    #     serializer.save(author=self.request.user, post=post)


class PostCommentList(ListAPIView):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentListSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        post = Post.objects.get(id=pk)
        return PostComment.objects.filter(post=post)


class PostLikeView(APIView):

    def post(self, request, pk):
        try:

            user = request.user
            post = Post.objects.get(id=pk)
            PostLike.objects.create(author=user, post=post)
            return Response({"success": "True"})
        except IntegrityError:
            return Response({"msg": "You already liked this post"})
