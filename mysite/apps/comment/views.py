from django.core.cache import cache
from django.views.generic import CreateView
from django.template.response import TemplateResponse
from django.http.response import JsonResponse


from .models import Comment
from .forms import CommentForm


class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "403.html"
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            captcha_text = request.POST.get("captcha", None)
            cached_captcha_text = cache.get(captcha_text, None)
        except KeyError:
            return JsonResponse(
                {"message": "No captcha", "status": 1}, status=400
            )
        else:
            if not cached_captcha_text:
                HTTP_404_NOT_FOUND = 404
                return JsonResponse(
                    {"message": "Invalid captcha", "status": 1},
                    status=HTTP_404_NOT_FOUND,
                )
            cache.set(key=captcha_text, value=captcha_text, timeout=0)
        return super(CreateCommentView, self).post(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return TemplateResponse(request, template=self.template_name)
