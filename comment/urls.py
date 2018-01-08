from django.conf.urls import url


from comment import views

app_name = 'comment'


urlpatterns = [
    url(r'new/$', views.create_comment),
]