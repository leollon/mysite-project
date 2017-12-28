import datetime
from django.template.library import Library

from article_category.models import ArticleCategory
from article.models import Article

register = Library()


# customize template tags
@register.simple_tag(name='category_numbers')
def count_category():
    """
    count the number of category
    :return: category number
    """
    return ArticleCategory.objects.count()


@register.simple_tag(name='article_numbers')
def count_article(user):
    """
    count the number of article
    :return: article number
    """
    return Article.objects.filter(author=user).count()


@register.simple_tag(name='newest_category')
def newest_cat():
    """
    get the newest 5 categories
    :return: return category_list
    """
    return ArticleCategory.objects.order_by('-created_time')[:6]


@register.simple_tag(name='newest_articles')
def newest_post(user):
    """
    get the user's newest 10 articles
    :param user:
    :return: article list
    """
    return Article.objects.filter(author=user)[:10]


@register.simple_tag(name='all_categories')
def all_category():
    """
    get all of Categories from category table
    :return: all of categories in database
    """
    return ArticleCategory.objects.all()


@register.simple_tag(name='all_articles')
def all_article(user):
    """
    get all of user's articles from article table
    :return:  all of articles
    """
    return Article.objects.filter(author=user).all()



@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


