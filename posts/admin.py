from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin

class PostCommentAdmin(MPTTModelAdmin):
    list_display = ("id", "post")
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = PostComment.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "caption")


admin.site.register(CommentLike)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostLike)
