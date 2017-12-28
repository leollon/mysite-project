from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from article.models import Article
from article_category.models import ArticleCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

per_page = getattr(settings, 'PER_PAGE')


@login_required
def manage_category(request):
    return render(request, 'category/category_backend.html')


def get_all_articles_by_category(request, category_id):
    """Get all articles by category
    :param
        @request: receive request from client
        @category_id: receive captured string from url
    :return: a response object with categorized articles
    """
    category = ArticleCategory.objects.get(pk=category_id)
    articles_list = Article.objects.order_by('-created_time').filter(
                                                        category_id=category_id)
    paginator = Paginator(articles_list, per_page=per_page)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request,
                  'category/article_categorized.html',
                  {"category": category, "articles": articles})


def get_all_category(request):
    category_lists = ArticleCategory.objects.all()
    return render(request, 'category/all_categories.html',
                  {'category_lists': category_lists})
