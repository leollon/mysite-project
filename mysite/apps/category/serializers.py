from rest_framework import serializers

from .models import ArticleCategory


class ArticleCategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleCategory
        exclude = ('id', 'created_time')
