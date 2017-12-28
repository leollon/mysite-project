from django.conf.urls import url

from users.views import login_view, logout_view
from users.views import register, validate_view, resend_email_view
from users.views import password_reset, password_reset_request
from users.views import dashboard


app_name = 'users'

urlpatterns = [
    url('^accounts/register/$', register, name='register'),
    url('^accounts/validate/(?P<token>[\w\-\.\^]+)', validate_view,
        name='validate'),

    url('^accounts/resend/$', resend_email_view, name='resend'),
    url('^accounts/login/$', login_view, name='login'),
    url('^accounts/logout/$', logout_view, name='logout'),

    url('^accounts/password_reset_request/$', password_reset_request,
        name='reset_request'),
    url('^accounts/password_reset/(?P<token>[\w\-\.\^]+)$', password_reset,
        name='pwd_reset'),
    url('^dashboard/$', dashboard, name='dashboard')
]
