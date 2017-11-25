from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    """
    Customize User model:
    make email field unique in users_user table
    """
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_active = models.BooleanField(_('active'),
                                    default=True,
                                    help_text=_('Designates whether this user \
                                    should be treated as active.Unselect this \
                                    instead of deleting accounts.'))
    is_staff = models.BooleanField(_('staff'),
                                   default=False,
                                   help_text=_('Designates whether the user \
                                               can log into this site'))

    class Meta:
        db_table = 'users_user'

    def __str__(self):
        return "%r" % self.username
