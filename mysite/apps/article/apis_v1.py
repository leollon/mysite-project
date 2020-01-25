from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleModelSerializer


class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)
