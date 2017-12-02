# -*- coding: utf-8 -*-
"""
customizing my own authentication system
"""

from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **credentials):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
