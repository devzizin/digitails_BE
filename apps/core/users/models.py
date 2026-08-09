
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Svitup.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
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



class CompanyUser(models.Model):
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
    position = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        db_table = "company_users"
 
    def __str__(self) -> str:
        return f"{self.user.email} ({self.position or 'no position'})"
