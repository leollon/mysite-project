from django.template.library import Library
from apps.category.models import ArticleCategory


register = Library()


# customize template tags
@register.simple_tag(name='category_numbers')
def count_category():
    """
    count the number of category
    :return: category number
    """
    return ArticleCategory.objects.count()


@register.simple_tag(name='newest_category')
def newest_cat():
    """
    get the newest 5 categories
    :return: return category_list
    """
    return ArticleCategory.objects.order_by('-created_time')[:6]


@register.simple_tag(name='all_categories')
def all_categories():
    """
    get all of Categories from category table
    :return: all of categories in database
    """
    return ArticleCategory.objects.all()
