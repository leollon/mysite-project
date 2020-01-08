from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from itsdangerous import BadTimeSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer


class User(AbstractUser):
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

    def generate_serializer(self):
        """
        generate a serial number for activating an account when a user
        register an account received a activate link in their email.
        :return: Serializer
        """
        return URLSafeTimedSerializer(settings.SECRET_KEY, salt=settings.SERIALIZER_SALT)

    def generate_valid_token(self):
        serializer = self.generate_serializer()
        return serializer.dumps({"pk": self.pk})

    def validate_account(self, token):
        serializer = self.generate_serializer()
        try:
            data = serializer.loads(token, max_age=settings.TOKEN_EXPIRES_IN)
        except (BadTimeSignature, SignatureExpired):
            return False

        if not isinstance(data, dict) or data.get("pk", None) != self.pk:
            return False

        self.is_valid = True
        self.save()
        return True

    def generate_email_token(self):
        serializer = self.generate_serializer()
        return serializer.dumps({"name": self.username}).decode(encoding="ascii")

    def verify_email_token(self, token):
        """Used to verify email token when reset a user's login password

        :type token: str
        :rtype: bool
        """
        serializer = self.generate_serializer()
        try:
            data = serializer.loads(token, max_age=settings.TOKEN_EXPIRES_IN)
        except (BadTimeSignature, SignatureExpired):
            return False

        if not isinstance(data, dict) or data.get("name", None) != self.username:
            return False
        return True

    class Meta:
        db_table = "auth_users"
