# -*- coding: utf-8 -*-
"""
extra feature:
    such as, processing account registered notification content,
    send email to user and so on.
"""

import os
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail


from mysite.settings import EMAIL_ACCOUNT


email_user = EMAIL_ACCOUNT.get('EMAIL_HOST_USER')
email_password = EMAIL_ACCOUNT.get('EMAIL_HOST_PASSWORD')


def get_notification():
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'notification')
    with open(file, 'r') as f:
        return f.read()


def get_user_info(request=None, form=None):
    if request is not None:
        username = request.user.username
        to_email = request.user.email
    elif form is not None:
        username = form.cleaned_data['username']
        to_email = form.cleaned_data['email']
    message = get_notification()
    return username, to_email, message


def notify_user(request=None, form=None, token=None):
    (username, to_email, message) = get_user_info(request, form)

    subject = _('Register an new account')
    from_email = email_user

    domain = 'http://127.0.0.1:8000'
    link = domain + "/accounts/validate/" + token
    html_message = message.format(username, link, link)

    send_mail(subject, message, from_email,
              [to_email],
              fail_silently=False,
              auth_user=email_user,
              auth_password=email_password,
              html_message=html_message)
