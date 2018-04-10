from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import BaseCreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

import mistune

from .forms import CreateArticleForm, EditArticleForm
from .utils import pager
from .my_renderer import HightlightRenderer
from .models import Article
from apps.comment.forms import CommentForm


class ArticleListView(ListView):
    """Index homepage
    """
    template_name = "article/index.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context['articles'] = pager(page)
        return context


class CreateArticleView(LoginRequiredMixin,
                        SingleObjectTemplateResponseMixin,
                        BaseCreateView):
    """Class-based view function used to write an article
    """
    template_name = 'article/editor.html'
    form_class = CreateArticleForm
    login_url = '/accounts/login/'

    def form_valid(self, form):
        """
        :param form: instantiate an form with request.POST
        :return: HttpResponseRedirect
        """
        # update article instance,
        # fix article'author is null when article posted.
        form.instance.author = self.request.user
        return super(CreateArticleView, self).form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UpdateView):
    """View function for editing a posted article
    """
    login_url = '/accounts/login/'
    template_name = 'article/editor.html'
    model = Article
    context_object_name = 'article'
    form_class = EditArticleForm

    # TODO: to be refactored in the future
    def get(self, request, *args, **kwargs):
        response = super(UpdateArticleView, self).get(request, *args, **kwargs)
        if request.user.is_superuser or request.user == self.object.author:
            return response
        return HttpResponseForbidden("<h1>The article can't be edited by you"
                                     ".</h1>")

    # TODO: to be refactored in the future
    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs.get('pk', None))
        if request.user.is_superuser or request.user == article.author:
            super(UpdateArticleView, self).post(request, *args, **kwargs)
            return HttpResponseRedirect(reverse("article:manage"))

        return HttpResponseForbidden("<h1>The article doesn't blog to "
                                     "you.</h1>")


class ArticleDetailView(DetailView, BaseCreateView):
    """The detail of each article
    """
    model = Article
    form_class = CommentForm
    template_name = 'article/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        renderer = HightlightRenderer()
        markdown = mistune.Markdown(escape=True,
                                    hard_wrap=True,
                                    renderer=renderer)
        article = super(ArticleDetailView, self).get_object()
        article.view_times += 1
        article.save()
        article.article_body = markdown(article.article_body)
        return article


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    login_url = 'account/login/'
    template_name = 'article/article_confirm.html'
    success_url = reverse_lazy('article:manage')
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(DeleteArticleView, self).get(request, *args, **kwargs)
        if self.object.author == request.user or request.user.is_superuser:
            return response
        return HttpResponseForbidden('<h1>This article does not blog to '
                                     'you.</h1>')

    def post(self, request, *args, **kwargs):
        response = super(DeleteArticleView, self).post(request, *args, **kwargs)
        if self.object.author == request.user or request.user.is_superuser:
            return response
        return HttpResponseForbidden('<h1>This article does not blog to '
                                     'you.</h1>')


class AllArticles(ListView):
    template_name = 'article/all_articles.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(AllArticles, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        per_page = 15
        context['articles'] = pager(page, per=per_page)
        return context


class ArticleManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'article/article_backend.html'


