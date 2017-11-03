# -*- coding: utf-8 -*-
from django.contrib import admin
from article_category.models import ArticleCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'count_number')
    list_filter = ('article_number',)
    ordering = ('article_number',)
    readonly_fields = ('article_number',)


admin.site.register(ArticleCategory, CategoryAdmin)


