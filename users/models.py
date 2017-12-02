from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from mysite import settings


@python_2_unicode_compatible
class User(AbstractUser):
    """
    Customize User model:
    make email field unique in users_user table
    """
    class Meta:
        db_table = 'users_user'

    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(_('staff'),
                                   default=False,
                                   help_text=_('Designates whether the user \
                                               can log into this site'))
    is_valid = models.BooleanField(_('validation'),
                                   default=False,
                                   help_text="Designates whether the user \
                                   will be blocked")
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "%s" % self.username

    def generate_serial(self, expires_in=1*24*60*60):
        """
        generate a serial number for activating an account when a user
        register an account received a activate link in their email.
        :return: Serial number
        """
        s = Serializer(getattr(settings, 'SERIAL_SECRET_KEY'), expires_in)
        return s

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


