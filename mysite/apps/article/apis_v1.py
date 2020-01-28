from rest_framework.response import Response
from rest_framework.views import APIView

from ..pagination import CustomizedCursorPagination
from .models import Article
from .serializers import ArticleModelSerializer


class ArticleAPIView(APIView):

    pagination_class = CustomizedCursorPagination

    def get(self, request):
        articles = Article.objects.all()
        page = self.pagination_class().paginate_queryset(articles, request)
        serializer = ArticleModelSerializer(page, many=True)
        return Response(serializer.data)
