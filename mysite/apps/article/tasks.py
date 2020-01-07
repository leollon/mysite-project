from celery import shared_task
from django.db.models import F

from .models import Article


@shared_task
def increment_user_view_times(article_id):
    return Article.objects.filter(id=article_id).update(
        user_view_times=F("user_view_times") + 1
    )


@shared_task
def increment_page_view_times(article_id):
    return Article.objects.filter(id=article_id).update(
        page_view_times=F("page_view_times") + 1
    )
