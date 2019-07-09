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
            captcha_text = request.POST.pop("captcha", None)
            cached_captcha_text = cache.get(captcha_text, None)
        except KeyError:
            pass
        else:
            if not cached_captcha_text:
                HTTP_404_NOT_FOUND = 404
                return JsonResponse(
                    {"message": "Invalid captcha", "status": 1},
                    status_code=HTTP_404_NOT_FOUND,
                )
        return super(CreateCommentView, self).post(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return TemplateResponse(request, template=self.template_name)
