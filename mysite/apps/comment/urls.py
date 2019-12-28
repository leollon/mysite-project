from django.conf.urls import url

from .views import CreateCommentView

app_name = "comment"

urlpatterns = [
    url("^new/$", CreateCommentView.as_view(), name="create")
]
