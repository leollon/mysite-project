from django.conf.urls import include, url

from .views import CreateCommentView


app_name = "comment"

urlpatterns = [
    # url(r'', include(router.urls)),
    url("^new/$", CreateCommentView.as_view(), name="create")
]
