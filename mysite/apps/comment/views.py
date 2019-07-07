from django.core.cache import cache
from django.views.generic import CreateView
from django.template.response import TemplateResponse


from .models import Comment
from .forms import CommentForm
from django.views.generic.base import TemplateResponse


class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "403.html"
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        return super(CreateCommentView, self).post(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return TemplateResponse(request, template=self.template_name)
