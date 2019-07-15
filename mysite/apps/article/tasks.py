from django.db.models import F
from celery import shared_task

from .models import Article

@shared_task
def increment_view_times(article_id):
    return Article.objects.filter(id=article_id).update(
        view_times=F("view_times") + 1
    )
