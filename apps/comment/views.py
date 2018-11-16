from django.core.cache import cache

from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Comment
from apps.article.models import Article
from .serializers import CommentSerializers


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 50


class CommentViewSets(mixins.CreateModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CommentSerializers
    pagination_class = CommentPagination
    queryset = Comment.objects.all()
    allowed_methods = ('GET', 'POST')

    def dispatch(self, request, *args, **kwargs):
        return super(CommentViewSets, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        try:
            key = Article.objects.get(pk=request.data.get('post'))
        except (KeyError, TypeError, Article.DoesNotExist) as e:
            msg = {'msg': 'Not Found', 'code': 404}
            return Response(
                msg,
                status=status.HTTP_404_NOT_FOUND,
                content_type="application/json; charset=utf-8")
        try:
            serializers.is_valid(raise_exception=True)
        except ValidationError as e:
            msg = {'msg': e.detail, 'code': 400}
            return Response(
                msg,
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json; charset=utf-8")
        else:
            self.perform_create(serializers)
            response = Response(
                serializers.data,
                status=status.HTTP_201_CREATED,
                content_type="application/json; charset=utf-8")
            return response

    def list(self, request, *args, **kwargs):
        response = super(CommentViewSets, self).list(request, *args, **kwargs)
        return response

    def perform_create(self, serializer):
        serializer.save()
