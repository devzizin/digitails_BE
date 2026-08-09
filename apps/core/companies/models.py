from django.db import models



class CompanyQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)

    def verified(self):
        return self.filter(is_verified=True)



class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.OneToOneField(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="company",
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
    )

    address_text = models.TextField(
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    website = models.TextField(
        null=True,
        blank=True,
    )

    logo_url = models.TextField(
        null=True,
        blank=True,
    )

    identification_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    is_verified = models.BooleanField(
        default=False,
        db_index=True,
    )

    secret_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    objects = CompanyQuerySet.as_manager()

    class Meta:
        db_table = "companies"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"], name="companies_name_idx"),
            models.Index(fields=["is_verified"], name="companies_verified_idx"),
            models.Index(fields=["deleted_at"], name="companies_deleted_idx"),
            models.Index(fields=["created_at"], name="companies_created_idx"),
            models.Index(
                fields=["identification_number"],
                name="companies_ident_num_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def has_user(
        self,
        *,
        email: str,
    ) -> bool:

        return self.user_links.filter(
            user__email=email.strip().lower(),
            user__deleted_at__isnull=True,
            deleted_at__isnull=True,
            is_active=True,
        ).exists()


