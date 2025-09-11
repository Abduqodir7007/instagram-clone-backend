from django.db import models
from django.core.validators import MaxLengthValidator
from users.models import User


class Post(models.Model):
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )
    caption = models.TextField(validators=[MaxLengthValidator(2000)])
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(validators=[MaxLengthValidator(500)])
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="child"
    )


class PostLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")


class CommentLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="likes"
    )
