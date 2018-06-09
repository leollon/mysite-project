from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import CommentViewSets

router = DefaultRouter()
router.register(r'comment', CommentViewSets, base_name='comment')

app_name = 'comment'

urlpatterns = [
    url(r'', include(router.urls)),
]
