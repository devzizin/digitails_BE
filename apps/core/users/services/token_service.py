import hashlib
import secrets
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.core.users.models import (
    User,
    AuthToken,
)
from apps.core.users.exceptions import (
    InvalidToken,
    TokenExpired,
    TokenAlreadyUsed,
    TokenRevoked,
)


class TokenService:

    DEFAULT_EXPIRATION_HOURS = 24

    @staticmethod
    def hash_token(
        raw_token: str,
    ) -> str:
        return hashlib.sha256(
            raw_token.encode(),
        ).hexdigest()

    @staticmethod
    @transaction.atomic
    def create(
        *,
        email: str,
        user: User | None = None,
        metadata: dict | None = None,
        expiration_hours: int | float |None = None,
    ) -> tuple[AuthToken, str]:
        """
        Create auth token and return:

        (
            token_instance,
            raw_token,
        )

        Raw token is returned only once.
        """

        raw_token = secrets.token_urlsafe(32)

        token_hash = TokenService.hash_token(
            raw_token,
        )

        expiration_hours = expiration_hours or TokenService.DEFAULT_EXPIRATION_HOURS

        token = AuthToken.objects.create(
            user=user,
            email=email.strip().lower(),
            token_hash=token_hash,
            metadata=metadata or {},
            expires_at=timezone.now()
            + timedelta(
                hours=expiration_hours,
            ),
        )

        return token, raw_token

    @staticmethod
    def validate(
        *,
        raw_token: str
    ) -> AuthToken:
        """
        Validate token and return token instance.
        """

        token_hash = TokenService.hash_token(
            raw_token,
        )

        token = (
            AuthToken.objects.select_related("user")
            .filter(
                token_hash=token_hash,
                deleted_at__isnull=True,
            )
            .first()
        )

        if not token:
            raise InvalidToken()

        if token.is_revoked:
            raise TokenRevoked()

        if token.is_consumed:
            raise TokenAlreadyUsed()

        if token.is_expired:
            raise TokenExpired()

        return token

    @staticmethod
    @transaction.atomic
    def consume(
        *,
        raw_token: str
    ) -> AuthToken:
        """
        Validate token and mark it as used.
        """

        token = TokenService.validate(
            raw_token=raw_token,
        )

        token.mark_used()

        return token

    @staticmethod
    @transaction.atomic
    def revoke(
        *,
        raw_token: str
    ) -> None:
        """
        Revoke active token.
        """

        token = TokenService.validate(
            raw_token=raw_token
        )

        token.revoke()