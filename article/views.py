from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from article.forms import CreateArticleForm, EditArticleForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

import mistune
from article.utils import pager
from article.my_renderer import HightlightRenderer
from article.models import Article


class ArticleList(ListView):
    """Index homepage
    """
    template_name = "article/index.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context['articles'] = pager(page)
        return context


class CreateArticleView(LoginRequiredMixin, CreateView):
    """Class-based view function used to write an article
    """
    template_name = 'article/article_write.html'
    form_class = CreateArticleForm
    login_url = '/accounts/login/'


class UpdateArticleView(LoginRequiredMixin, UpdateView):
    """View function for editing a posted article
    """
    login_url = '/accounts/login/'
    template_name = 'article/article_write.html'
    model = Article
    context_object_name = 'article'
    form_class = EditArticleForm

    # TODO: to be refactored in the future
    def get(self, request, *args, **kwargs):
        response = super(UpdateArticleView, self).get(request, *args, **kwargs)
        if request.user != self.object.author or not request.user.is_superuser:
            return HttpResponseForbidden("<h1>The article doesn't blog to "
                                         "you.</h1>")
        return response

    # TODO: to be refactored in the future
    def post(self, request, *args, **kwargs):
        super(UpdateArticleView, self).post(request, *args, **kwargs)
        if request.user != self.object.author or not request.user.is_superuser:
            return HttpResponseForbidden("<h1>The article doesn't blog to "
                                         "you.</h1>")
        return HttpResponseRedirect(reverse("article:index"))
    

class ArticleDetailView(DetailView):
    """The detail of each article
    """
    model = Article
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


class AllArticles(ListView):
    template_name = 'article/all_articles.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(AllArticles, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        per_page = 10
        context['articles'] = pager(page, per=per_page)
        return context
