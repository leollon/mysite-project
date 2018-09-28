from .views import CommentViewSets
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comment', CommentViewSets, base_name='comment')

app_name = 'comment'

urlpatterns = [
    url(r'', include(router.urls)),
]
