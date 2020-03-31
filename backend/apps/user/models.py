from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixins import UserMixins


class User(UserMixins, AbstractUser):
    """
    Customize User model:
    make email field unique in auth_user table
    """

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff"),
        default=False,
        help_text=_("Designates whether the user can log into this site"),
    )
    is_valid = models.BooleanField(
        _("validation"),
        default=False,
        help_text="Designates whether the user will be blocked",
    )
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "%s" % self.username

    class Meta:
        db_table = "auth_users"
