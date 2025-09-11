from django.contrib import admin
from .models import *

admin.site.register(CommentLike)
admin.site.register(PostComment)
admin.site.register(Post)
admin.site.register(PostLike)
