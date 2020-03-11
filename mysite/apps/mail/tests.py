from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.utils.translation import ugettext as _

from .models import EmailRecord
from .tasks import send_email


class TestEmailRecordModel(TestCase):

    def test_create_email_record_success(self):
        pass

    def test_create_email_record_failure(self):
        pass


class TestSendEmail(TestCase):

    def setUp(self) -> None:
        self.email = 'email@gmail.com'
        self.subject = _('test send mail')

    def test_send_email_success(self):

        context = {
            'link': ''.join((settings.FRONTEND_HOST, '/articles/abcd', )), 'title': 'abcd',
            'comment': 'test send email', 'username': 'send email'}
        send_email(
            email=self.email, subject=self.subject,
            ip='127.0.0.1', template_name='comment/comment_mail_msg.tpl',
            context=context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, _('test send mail'))
        record = EmailRecord.objects.all().last()
        self.assertEqual(record.username, 'send email')

    def test_send_email_failure(self):

        pass
