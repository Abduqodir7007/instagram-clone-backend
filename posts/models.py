from django.db import models
from django.core.validators import MaxLengthValidator
from users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from users.models import BaseModel

class Post(BaseModel):
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )
    caption = models.TextField(validators=[MaxLengthValidator(2000)])
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.author.username}'s post"

    class Meta:
        ordering = ["-id"]


class PostComment(MPTTModel, BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(validators=[MaxLengthValidator(500)])
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="child"
    )


class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")


class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="likes"
    )
