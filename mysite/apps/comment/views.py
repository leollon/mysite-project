from django.conf import settings
from django.db.models import Q
from rest_framework import generics

from .models import Comment
from .serializers import CommentModelSerializer

from apps.article.models import Article  # noqa: isort:skip
from apps.mail.tasks import send_email  # noqa: isort:skip
from apps.core import CustomizedCursorPagination  # noqa: isort:skip

email = settings.EMAIL_HOST_USER


class CommentListAPIView(generics.ListAPIView, generics.CreateAPIView):

    http_method_names = ('get', 'post', 'options', )
    lookup_filed = lookup_url_kwargs = 'slug'

    serializer_class = CommentModelSerializer
    pagination_class = CustomizedCursorPagination

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_filed)
        queryset = Comment.objects.filter(Q(post__slug=slug))
        return queryset
