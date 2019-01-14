"""
extra feature:
    such as, processing account registered notification content,
    send email to user and so on.
"""

import os

from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from mysite.config.settings.develop import DOMAIN_NAME, EMAIL_ACCOUNT

email_user = EMAIL_ACCOUNT.get('EMAIL_HOST_USER')
email_password = EMAIL_ACCOUNT.get('EMAIL_HOST_PASSWORD')


def get_notification(filename):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(file, 'r') as f:
        return f.read()


def get_user_info(request, filename):
    username = request.POST.get('username', request.user.username)
    if request.method == "POST":
        to_email = request.POST.get('email')
    else:
        to_email = request.user.email
    message = get_notification(filename)
    return username, to_email, message


def notify_user(request, **kwargs):
    (username, to_email, message) = get_user_info(request,
                                                  kwargs.get('filename'))

    subject = _(kwargs.get('subject'))
    from_email = email_user

    domain = DOMAIN_NAME
    link = domain + kwargs.get('url') + kwargs.get('token')
    html_message = message.format(username, link, link)

    send_mail(
        subject,
        message,
        from_email, [to_email],
        fail_silently=False,
        auth_user=email_user,
        auth_password=email_password,
        html_message=html_message)
