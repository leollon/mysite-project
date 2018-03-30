from django.contrib import admin
from .models import Comment


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
