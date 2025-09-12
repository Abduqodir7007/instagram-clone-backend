from rest_framework import serializers
from .models import *

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField()
    image = serializers.ImageField(read_only=True)


class PostSerilalizer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField("count_likes")
    post_comments = serializers.SerializerMethodField("count_post_comments")
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "caption", "image", "author", "likes", "post_comments"]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def count_likes(self, obj):
        return obj.likes.count()

    def count_post_comments(self, obj):
        return obj.comments.count()
    
class PostCommentViewSerializer(serializers.Serializer):
    comment = serializers.CharField()

    
    def create(self, validated_data):
        return PostComment.objects.create(**validated_data)
