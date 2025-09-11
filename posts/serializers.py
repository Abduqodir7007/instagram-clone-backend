from rest_framework import serializers
from .models import Post


class PostSerilalizer(serializers.Serializer):
    caption = serializers.CharField()
    image = serializers.ImageField()
    likes = serializers.SerializerMethodField("count_likes")
    post_comments = serializers.SerializerMethodField("count_post_comments")

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def count_likes(self, obj):
        return obj.likes.count()

    def count_post_comments(self, obj):
        return obj.comments.count()
