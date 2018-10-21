from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from mysite.config.settings import dev_settings


@python_2_unicode_compatible
class User(AbstractUser):
    """
    Customize User model:
    make email field unique in users_user table
    """

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff'),
        default=False,
        help_text=_('Designates whether the user \
                                               can log into this site'))
    is_valid = models.BooleanField(
        _('validation'),
        default=False,
        help_text="Designates whether the user \
                                   will be blocked")
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "%s" % self.username

    def generate_serial(self, expires_in=3600):
        """
        generate a serial number for activating an account when a user
        register an account received a activate link in their email.
        :param expires_in: after that seconds, token will be valid
        :return: Serial number
        """
        return Serializer(
            getattr(dev_settings, 'SERIAL_SECRET_KEY'), expires_in)

    def generate_valid_token(self):
        serial_number = self.generate_serial()
        return serial_number.dumps({'pk': self.id}).decode(encoding='ascii')

    def valid_account(self, token):
        serial_number = self.generate_serial()
        try:
            data = serial_number.loads(token)
        except:
            return False

        if data.get('pk') != self.id:
            return False

        self.is_valid = True
        self.save()
        return True

    def generate_email_token(self):
        serial_obj = self.generate_serial(expires_in=1 * 24 * 60 * 60)
        return serial_obj.dumps({
            'name': self.username
        }).decode(encoding="ascii")

    def verify_email_token(self, token):
        serial_obj = self.generate_serial(expires_in=30 * 60)
        try:
            data = serial_obj.loads(token)
        except:
            return False

        if data.get('name') != self.username:
            print(data.get('name'))
            return False
        return True

    class Meta:
        db_table = 'auth_users'
