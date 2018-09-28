"""
customizing my own authentication system
"""

from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **credentials):
        UserModel = User
        try:
            user = UserModel.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
