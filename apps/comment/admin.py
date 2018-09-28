from .models import Comment
from django.contrib import admin

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    """
    make CommentModel edited in  default django backend for emergency.
    """
    list_display = ('username', 'email', 'link', 'comment_text', 'post',
                    'created_time', )
    ordering = ('username', 'created_time', )
    list_filter = ('username', 'created_time', )
    search_fields = ('username', )


admin.site.register(Comment, CommentAdmin)
