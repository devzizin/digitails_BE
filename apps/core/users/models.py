import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Svitup.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    uuid = models.UUIDField(
            unique=True, 
            default=uuid.uuid4, 
            editable=False, 
            db_index=True,
        )
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First name"), blank=True, max_length=150)
    last_name = CharField(_("Last name"), blank=True, max_length=150)
    phone = CharField(_("Phone number"), blank=True, max_length=32)
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.name


class UserCompany(models.Model):
    """Staff profile for a User within the company.

    Kept separate from User to isolate auth/identity concerns (email,
    password) from company-staff concerns (position, activity status,
    assigned roles). Created alongside User on registration/invite.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company_profile",
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="user_links",
    )
    position = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "company_users"

    def __str__(self) -> str:
        return f"{self.user.email} ({self.position or 'no position'})"


class AuthTokenQuerySet(models.QuerySet):

    def active(self):
        return self.filter(
            used_at__isnull=True,
            revoked_at__isnull=True,
            deleted_at__isnull=True,
            expires_at__gt=timezone.now(),
        )

    def active_for_email(
        self,
        *,
        email: str,
    ):
        return self.active().filter(
            email=email.strip().lower(),
        )

    def for_email(self, email: str):
        return self.filter(
            email=email.strip().lower(),
        )


class AuthToken(models.Model):

    objects = AuthTokenQuerySet.as_manager()

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="auth_tokens",
        null=True,
        blank=True,
        help_text="""
        Optional user linked to the token.

        Invitation tokens may exist before a user account
        has been created.
        """,
    )

    email = models.EmailField(
        db_index=True,
        help_text="""
        Target email address associated with the token.
        """,
    )

    token_hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="""
        SHA256 hash of the raw token.

        Raw token is never stored.
        """,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Arbitrary token-specific data.

        Examples:

        Invitation:
            {
                "company_id": 1
            }

        Change email:
            {
                "new_email": "new@test.com"
            }
        """,
    )

    expires_at = models.DateTimeField(
        db_index=True,
        help_text="""
        Token expiration timestamp.
        """,
    )

    used_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="""
        Set once token is consumed.

        Prevents token reuse.
        """,
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="""
        Token manually revoked before expiration.
        """,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="""
        Soft-delete timestamp.
        """,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "auth_tokens"
        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "email",
                ]
            ),
            models.Index(
                fields=[
                    "expires_at",
                ]
            ),
            models.Index(
                fields=[
                    "token_hash",
                ]
            ),
        ]

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_consumed(self) -> bool:
        return self.used_at is not None

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @property
    def is_active(self) -> bool:
        return (
            not self.is_consumed
            and not self.is_revoked
            and not self.is_expired
            and not self.is_deleted
        )

    @property
    def status(self) -> str:
        if self.used_at:
            return "used"

        if self.revoked_at:
            return "revoked"

        if self.expires_at <= timezone.now():
            return "expired"

        return "pending"

    def mark_used(self) -> None:
        if self.used_at is None:
            self.used_at = timezone.now()

            self.save(
                update_fields=[
                    "used_at",
                    "updated_at",
                ]
            )

    def revoke(self) -> None:
        if self.revoked_at is None:
            self.revoked_at = timezone.now()

            self.save(
                update_fields=[
                    "revoked_at",
                    "updated_at",
                ]
            )

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()

        super().save(*args, **kwargs)