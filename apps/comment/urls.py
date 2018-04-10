from django.conf.urls import url


from .views import create_comment

app_name = 'comment'


urlpatterns = [
    url(r'new/$', create_comment),
]