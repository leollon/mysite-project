from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseNotFound
from rest_framework import generics
from rest_framework.response import Response
from utils import cache

from .models import Comment
from .serializers import CommentModelSerializer

from apps.article.models import Article  # noqa: isort:skip
from apps.mail.tasks import send_email  # noqa: isort:skip
from apps.core import CustomizedCursorPagination  # noqa: isort:skip

email = settings.EMAIL_HOST_USER


class ArticleCommentListAPIView(generics.ListAPIView, generics.CreateAPIView):

    http_method_names = ('get', 'post', 'options', )
    lookup_filed = lookup_url_kwargs = 'slug'

    serializer_class = CommentModelSerializer
    pagination_class = CustomizedCursorPagination

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_filed)
        queryset = Comment.objects.filter(Q(post__slug=slug))
        return queryset

    def get(self, request, *args, **kwargs):
        return super(ArticleCommentListAPIView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        captcha_text = request.POST.get('captcha', None)
        cached_captcha_text = None
        if captcha_text:
            cached_captcha_text = cache.get(captcha_text.lower(), None)
        if not cached_captcha_text:
            return Response(
                data={'message': 'Invalid captcha'},
                status=HttpResponseNotFound.status_code,
            )
        cache.delete(key=captcha_text)
        comment = request.POST.get('comment_text', None)
        ip = request.META.get('REMOTE_ADDR')
        username = request.POST.get('username', ip)
        article_id = request.POST.get('post', None)
        try:
            article = Article.objects.get(pk=article_id)
        except (Article.DoesNotExist, Exception):
            return Response(
                data={'message': 'The article does not exist.'},
                status=HttpResponseNotFound.status_code)
        else:
            link = ''.join((settings.FRONTEND_HOST, '/articles/', article.slug, ))
            context = {'username': username or ip, 'link': link, 'title': article.title, 'comment': comment}
        subject = "Having a new comment on '%s'" % (article.title)
        send_email.delay(
            email=email, subject=subject, ip=ip,
            template_name='comment/comment_mail_msg.tpl', context=context)
        return super(ArticleCommentListAPIView, self).post(request, *args, **kwargs)
