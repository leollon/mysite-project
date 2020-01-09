from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseNotFound
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import CreateView

from .forms import CommentForm
from .models import Comment

from apps.article.models import Article  # noqa: isort:skip
from apps.mail.tasks import send_email  # noqa: isort:skip

email = settings.EMAIL_HOST_USER


class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "403.html"
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        captcha_text = request.POST.get("captcha", None)
        cached_captcha_text = cache.get(captcha_text, None)
        if not cached_captcha_text:
            return JsonResponse(
                data={"message": "Invalid captcha", "status": 1},
                status=HttpResponseNotFound.status_code,
            )
        cache.set(key=captcha_text, value=captcha_text, timeout=0)
        username = request.POST.get("username", None)
        comment = request.POST.get("comment_text", None)
        ip = request.META.get("REMOTE_ADDR")
        article_id = request.POST.get("post", None)
        try:
            article = Article.objects.get(pk=article_id)
        except (Article.DoesNotExist, Exception):
            return JsonResponse(
                data={"message": "The article does not exist."},
                status=HttpResponseNotFound.status_code)
        else:
            link = "".join((settings.HOST, reverse("article:detail", args=(article.slug,))))
            context = {"username": username or ip, "link": link, "title": article.title, "comment": comment}
        subject = "Having a new comment on '%s'" % (article.title)
        if username:
            send_email.delay(
                email=email, subject=subject, ip=ip,
                template_name="comment/comment_mail_msg.tpl", context=context)
        return super(CreateCommentView, self).post(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return TemplateResponse(request, template=self.template_name)
