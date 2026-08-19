from __future__ import annotations

from django.contrib.auth.backends import ModelBackend

from apps.core.users.models import User


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, identifier=None, password=None, **kwargs):
        login_value = identifier or email or username
        if not login_value or not password:
            return None

        login_value = login_value.strip().lower()

        try:
            user = User.objects.get(email=login_value)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

        if not user.is_active:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None