from django.contrib import admin
from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    """
        Article model should be editable in thd admin interface.
    """
    list_display = ('title', 'article_body', 'category', 'created_time')
    list_filter = ('created_time', 'view_times')
    ordering = ('created_time', 'view_times')
    readonly_fields = ('view_times',)
    search_fields = ('title',)


admin.site.register(Article, ArticleAdmin)
