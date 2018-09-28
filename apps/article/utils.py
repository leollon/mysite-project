from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Article

per_page = getattr(settings, 'PER_PAGE')


def pager(page, per=per_page):
    """
    paginate a huge possibly article list
    :param page: current page number
    :param per: the number of article per page
    :return: an article list
    """
    articles_list = Article.objects.order_by('-created_time').all()
    # paginator paginate an ordered list
    paginator = Paginator(articles_list, per_page=per)
    page = page
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return articles
