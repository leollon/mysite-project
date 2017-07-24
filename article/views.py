from django.views.generic import DetailView
from article.models import Article
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView


class ArticleDetail(DetailView):
    """
    the detail of each article
    """
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        article = super(ArticleDetail, self).get_object()
        article.view_times += 1
        article.save()
        return article


class ArticleList(ListView):
    """
    index homepage
    """
    template_name = "index.html"
    context_object_name = 'article_list'
    model = Article


class ArticleCreate(CreateView):
    """
    class-based view function used to write an article
    """
    template_name = 'article_form.html'
    model = Article
    fields = ['title', 'article_body']


class ArticleUpdate(UpdateView):
    """
    view function for editing a posted article
    """
    template_name = 'article_edit.html'
    model = Article
    context_object_name = 'article'
    fields = ['title', 'article_summary', 'article_body']

    def get_object(self):
        article = super(ArticleUpdate, self).get_object()
        return article


