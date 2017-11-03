from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from article.forms import CreateArticleForm, EditAriticleForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

import mistune
from article.utils import HightlightRenderer
from article.models import Article

per_page = getattr(settings, 'PER_PAGE')


class ArticleList(ListView):
    """Index homepage
    """
    template_name = "index.html"
    model = Article
    context_object_name = 'articles_list'

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        articles_list = Article.objects.order_by('-created_time').all()
        renderer = HightlightRenderer()
        markdown = mistune.Markdown(escape=True, hard_wrap=True,
                                    renderer=renderer)
        # paginator paginate an ordered list
        paginator = Paginator(articles_list, per_page=per_page)
        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
            for article in articles:
                article.article_body = markdown(article.article_body)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        context['articles'] = articles
        return context


class CreateArticleView(CreateView):
    """Class-based view function used to write an article
    """
    template_name = 'article_write.html'
    form_class = CreateArticleForm


class UpdateArticleView(UpdateView):
    """View function for editing a posted article
    """
    template_name = 'article_write.html'
    model = Article
    context_object_name = 'article'
    form_class = EditAriticleForm
    # fields = ['title', 'article_body']

    def get_object(self):
        article = super(UpdateArticleView, self).get_object()
        return article


class ArticleDetailView(DetailView):
    """The detail of each article
    """
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        renderer = HightlightRenderer()
        markdown = mistune.Markdown(escape=True, hard_wrap=True, renderer=renderer)
        article = super(ArticleDetailView, self).get_object()
        article.view_times += 1
        article.save()
        article.article_body = markdown(article.article_body)
        return article
