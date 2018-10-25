import mistune
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseCreateView, DeleteView, UpdateView
from django.core.paginator import Paginator

from .forms import CreateArticleForm, EditArticleForm
from .models import Article
from .my_renderer import HightlightRenderer
from .utils import pager
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


class CreateArticleView(LoginRequiredMixin, SingleObjectTemplateResponseMixin,
                        BaseCreateView):
    """Class-based view function used to write an article
    """
    template_name = 'article/editor.html'
    form_class = CreateArticleForm
    login_url = '/accounts/login/'

    def dispatch(self, request, *args, **kwargs):
        return super(CreateArticleView, self).dispatch(request, *args,
                                                       **kwargs)

    def form_valid(self, form):
        """
        :param form: instantiate an form with request.POST
        :return: HttpResponseRedirect
        """
        # update article instance,
        # fix article'author is null when article posted.
        form.instance.author = self.request.user
        return super(CreateArticleView, self).form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View function for editing a posted article
    """
    model = Article
    login_url = '/accounts/login/'
    template_name = 'article/editor.html'
    context_object_name = 'article'
    form_class = EditArticleForm
    permission_denied_message = "Permission Denied."
    raise_exception = True

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or \
            self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return super(UpdateArticleView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super(UpdateArticleView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse("articles:manage"))


class ArticleDetailView(DetailView, BaseCreateView):
    """The detail of each article
    """
    model = Article
    form_class = CommentForm
    template_name = 'article/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        renderer = HightlightRenderer()
        markdown = mistune.Markdown(
            escape=True, hard_wrap=True, renderer=renderer)
        article = super(ArticleDetailView, self).get_object()
        article.view_times += 1
        article.save()
        article.article_body = markdown(article.article_body)
        return article


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    login_url = 'account/login/'
    template_name = 'article/article_confirm.html'
    success_url = reverse_lazy('article:manage')
    context_object_name = 'article'
    permission_denied_message = "Permission Denied."
    raise_exception = True

    def test_func(self):
        article = self.get_object()
        return self.request.user == articl.author or \
            self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return super(DeleteArticleView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(DeleteArticleView, self).post(request, *args, **kwargs)


class AllArticles(ListView):
    template_name = 'article/all_articles.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(AllArticles, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        per_page = 15
        context['articles'] = pager(page, per=per_page)
        return context


class TaggedArticleListView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'articles'

    def get_queryset(self, **kwargs):
        queryset = Article.objects.filter(
            tags__icontains=self.kwargs.get('tag'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaggedArticleListView, self).get_context_data(**kwargs)
        return context


class ArticleManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'article/article_backend.html'
