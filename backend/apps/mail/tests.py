import random
import string

from django.conf import settings
from django.core import mail
from django.db.utils import DataError
from django.test import TestCase
from django.utils.translation import ugettext as _

from .models import EmailRecord
from .tasks import send_email


class TestEmailRecordModel(TestCase):

    def test_create_email_record_success(self):

        record = EmailRecord.objects.create(
            username='123456', mail_message='123456 leaves a comment',
            ip='127.0.0.1', mail_state='success', reason='')
        self.assertEqual(EmailRecord.objects.all().last().username, record.username)

        record = EmailRecord.objects.create(
            username='halo', mail_message='halo leaves a comment',
            ip='192.168.10.1', mail_state='success', reason='')
        self.assertEqual(EmailRecord.objects.all().last().username, record.username)

    def test_create_email_record_failure_with_too_long_username(self):

        # too long username
        try:
            EmailRecord.objects.create(
                username=''.join(
                    [random.choice(string.digits + string.ascii_letters) for _ in range(65)]),
                mail_message='too long username', ip='19.19.19.100', mail_state='error',
                reason='value too long for type character varying(64)')
        except DataError:
            self.assertRaises(DataError)

    def test_create_email_record_failure_with_too_long_mail_state(self):

        # too long mail state
        try:
            EmailRecord.objects.create(
                username='too long mail state', mail_message='too long mail state',
                mail_state=''.join(random.sample(string.ascii_letters + string.digits, random.randint(17, 62))),
                reason='value too long for type character varying(16)')
        except DataError:
            self.assertRaises(DataError)


class TestSendEmailTask(TestCase):

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

        self.email = 'email@gmail.com'
        context = {
            'link': ''.join((settings.FRONTEND_HOST, '/articles/abcdef',), ), 'title': 'abcdef',
            'comment': 'fail to send email', 'username': 'failure test send email'}

        with self.settings(EMAIL_BACKEND=''):
            send_email(
                email=self.email, subject=self.subject,
                ip='127.0.0.1', template_name='comment/comment_mail_msg.tpl',
                context=context)

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(EmailRecord.objects.all().last().username, 'failure test send email')
        self.assertNotEqual(EmailRecord.objects.all().last().reason, '')
