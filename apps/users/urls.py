from django.conf.urls import url

from .views import (dashboard, login_view, logout_view, password_reset,
                    password_reset_request, register, resend_email_view,
                    validate_view)

app_name = 'users'

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^validate/(?P<token>[\w\-\.\^]+)', validate_view,
        name='validate'),

    url(r'^resend/$', resend_email_view, name='resend'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^password_reset_request/$', password_reset_request,
        name='reset_request'),
    url(r'^password_reset/(?P<token>[\w\-\.\^]+)$', password_reset,
        name='pwd_reset'),
    url(r'^dashboard/$', dashboard, name='dashboard')
]
