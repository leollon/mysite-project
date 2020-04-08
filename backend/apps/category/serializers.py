from rest_framework import serializers

from .models import ArticleCategory


class ArticleCategoryModelSerializer(serializers.ModelSerializer):

    article_statistics = serializers.IntegerField()

    class Meta:
        model = ArticleCategory
        exclude = ('id', 'created_time')
