# -*- coding: utf-8 -*-
from django.contrib import admin
from article_category.models import ArticleCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_number', 'created_time')
    ordering = ('created_time', )


admin.site.register(ArticleCategory, CategoryAdmin)


