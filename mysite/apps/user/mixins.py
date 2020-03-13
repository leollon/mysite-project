from django.conf import settings
from itsdangerous import BadTimeSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer


class UserMixins:

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
