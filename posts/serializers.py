from rest_framework import serializers
from .models import *


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField()
    image = serializers.ImageField(read_only=True)


class PostSerilalizer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField("count_likes")
    post_comments = serializers.SerializerMethodField("count_post_comments")
    liked = serializers.SerializerMethodField("me_liked")
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "caption",
            "image",
            "author",
            "likes",
            "post_comments",
            "liked",
        ]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def count_likes(self, obj):
        return obj.likes.count()

    def count_post_comments(self, obj):
        return obj.comments.count()

    def me_liked(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:
                if PostLike.objects.get(author=request.user, post=obj):
                    return True
            except PostLike.DoesNotExist:
                return False
        return False


class PostCommentCreateSerializer(serializers.Serializer):
    comment = serializers.CharField()

    def create(self, validated_data):
        return PostComment.objects.create(**validated_data)


class PostCommentListSerializer(serializers.Serializer):
    author = UserSerializer(read_only=True)
    comment = serializers.CharField()
    created_at = serializers.DateTimeField()
    parent = serializers.IntegerField(required=False, allow_null=True)
    # replies = serializers.SerializerMethodField('get_replies')

    # def get_replies(self, obj):
    #     if obj.child.exists():
    #         serializer = self.__class__(obj.child.all(), many=True, context=self.context)


class CommentSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField("get_like_counts")
    replies = serializers.SerializerMethodField("get_replies")
    liked = serializers.SerializerMethodField("me_liked")
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = [
            "comment",
            "post",
            "author",
            "created_at",
            "likes",
            "replies",
            "liked",
        ]

    def get_like_counts(self, obj):
        return obj.likes.count()

    def me_liked(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:
                if CommentLike.objects.get(comment=obj, author=request.user):
                    return True
            except CommentLike.DoesNotExist:
                return False

    def get_replies(self, obj):
        if obj.child.exists():
            serializer = self.__class__(
                obj.child.all(), many=True, context=self.context
            )
            return serializer.data
        return None
    
class CommentCreateSerializer(serializers.Serializer):
    comment = serializers.CharField()
    post_id = serializers.UUIDField()
    comment_id= serializers.UUIDField()
    
    def create(self, validated_data):
        return PostComment.objects.create(**validated_data)
