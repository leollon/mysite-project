import smtplib
import socket

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .models import EmailRecord

email_user = settings.EMAIL_HOST_USER
email_password = settings.EMAIL_HOST_PASSWORD


@shared_task
def send_email(email, subject, ip, template_name, context):
    to_email = email
    html_message = message = render_to_string(template_name, context=context)

    subject = _(subject)
    from_email = email_user

    try:
        send_mail(
            subject, message, from_email, [to_email],
            fail_silently=False, auth_user=email_user,
            auth_password=email_password, html_message=html_message,
        )
        state, reason = 'success', ''
    except (smtplib.SMTPException, socket.error, Exception) as e:
        state, reason = 'error', e.args[0]
    finally:
        EmailRecord.objects.create(
            username=context.get("username")[:64], mail_message=html_message,
            ip=ip, mail_state=state, reason=reason
        )
