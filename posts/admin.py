from django.contrib import admin
from .models import *


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post")


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "caption")


admin.site.register(CommentLike)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostLike)
