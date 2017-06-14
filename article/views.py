from django.views.generic import DetailView
from article.models import Article
from django.views.generic import ListView
from django.views.generic.edit import CreateView


class ArticleDetail(DetailView):
    """
    the detail of each article
    """
    queryset = Article.objects.all()
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
    fields = ['title', 'article_summary', 'article_body']


