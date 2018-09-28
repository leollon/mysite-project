from .models import ArticleCategory
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_number', 'created_time')
    ordering = ('created_time', )


admin.site.register(ArticleCategory, CategoryAdmin)
