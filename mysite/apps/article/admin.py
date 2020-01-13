from django.contrib import admin
from django.template.defaultfilters import truncatechars_html

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    """
        Article model should be editable in thd admin interface.
    """
    list_display = ('title', 'article_preview', 'category', 'created_time')
    list_filter = ('created_time', 'user_view_times', 'page_view_times', )
    ordering = ('created_time', 'user_view_times', 'page_view_times', )
    readonly_fields = ('user_view_times', 'page_view_times', 'slug', )
    search_fields = ('title',)
    list_per_page = 15

    def article_preview(self, article):
        return truncatechars_html(article.article_body, '140')


admin.site.register(Article, ArticleAdmin)
