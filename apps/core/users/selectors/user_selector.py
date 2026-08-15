from uuid import UUID

from django.db.models import Prefetch

from apps.core.users.exceptions import UserNotFound
from apps.core.users.models import User


class UserSelector:

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user = User.objects.filter(
            id=user_id,
            deleted_at__isnull=True,
        ).first()

        if not user:
            raise UserNotFound()

        return user


    @staticmethod
    def get_user_by_uuid(
        user_uuid: UUID,
        with_organisations: bool = False,
    ) -> User:

        queryset = User.objects.filter(
            uuid=user_uuid,
            deleted_at__isnull=True,
        )


        user = queryset.first()

        if not user:
            raise UserNotFound()

        return user

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return User.objects.filter(
            email=email.strip().lower(),
            deleted_at__isnull=True,
        ).first()

