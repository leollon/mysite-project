from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from .utils import get_notification

host = getattr(settings, "HOST")
email_user = getattr(settings, "EMAIL_HOST_USER")
email_password = getattr(settings, "EMAIL_HOST_PASSWORD")


@shared_task
def notify_user(username, email, **kwargs):
    username, to_email = username, email
    message = get_notification(kwargs.get("filename"))

    subject = _(kwargs.get("subject"))
    from_email = email_user

    link = host + kwargs.get("url") + kwargs.get("token")
    html_message = message.format(username, link, link)

    return send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
        auth_user=email_user,
        auth_password=email_password,
        html_message=html_message,
    )
