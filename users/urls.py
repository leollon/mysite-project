from django.conf.urls import url
from users.views import login_view, logout_view, register, \
                        password_reset,password_reset_request

app_name = 'users'

urlpatterns = [
    url('^login/$', login_view, name='login'),
    url('^logout/$', logout_view, name='logout'),
    url('^register/$', register),
    url('^password_reset_request/$', password_reset_request,
        name='reset_request'),
    url('^password_reset/$', password_reset, name='reset'),
]
