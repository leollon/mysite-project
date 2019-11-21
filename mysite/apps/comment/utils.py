import os

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from apps.article.models import Article

HOST = getattr(settings, "HOST")
EMAIL_RELATED = getattr(settings, "EMAIL_RELATED")
message_template_file = EMAIL_RELATED.get("COMMENT_NOTIFICATION")
email_address = getattr(settings, "EMAIL_HOST_USER")
email_password = getattr(settings, "EMAIL_HOST_PWD")


def message_handle(filename, **kwargs):
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), filename
    )
    with open(filename) as f:
        message = f.read()
        article_link = HOST + reverse(
            "article:detail", kwargs={"pk": kwargs.get("article_id")}
        )
        message = message.format(
            kwargs.get("username"),
            article_link,
            kwargs.get("title"),
            kwargs.get("comment_content"),
        )
        return message


def send_comment_notification_to_site_owner(
    article_id, username, comment_content
):
    subject = Article.objects.get(id=article_id).title
    message = message_handle(
        message_template_file,
        username=username,
        article_id=article_id,
        title=subject,
        comment_content=comment_content,
    )
    send_mail(
        subject,
        message,
        email_address,
        [email_address],
        auth_user=email_address,
        auth_password=email_password,
        html_message=message,
    )
