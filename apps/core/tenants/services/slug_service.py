import re

from slugify import slugify

from apps.core.tenants.models import Tenant


class SlugService:

    RESERVED = {"admin", "api", "root", "public"}

    @classmethod
    def normalize_schema(cls, value: str) -> str:
        value = slugify(value or "").lower()
        value = value.replace("-", "_")
        value = re.sub(r"[^a-z0-9_]", "", value)

        if value and value[0].isdigit():
            value = f"t_{value}"

        return value

    @classmethod
    def normalize_domain(cls, value: str) -> str:
        value = slugify(value or "").lower()
        value = re.sub(r"[^a-z0-9-]", "", value)

        if value and value[0].isdigit():
            value = f"t-{value}"

        return value

    @classmethod
    def ensure_schema_not_reserved(cls, slug: str) -> str:
        if slug in cls.RESERVED:
            return f"{slug}_tenant"

        return slug

    @classmethod
    def ensure_domain_not_reserved(cls, slug: str) -> str:
        if slug in cls.RESERVED:
            return f"{slug}-tenant"

        return slug

    @classmethod
    def prepare_schema(cls, name: str, slug: str | None = None) -> str:
        value = slug or name

        prepared_slug = cls.normalize_schema(value)

        if not prepared_slug:
            prepared_slug = "tenant"

        return cls.ensure_schema_not_reserved(prepared_slug)

    @classmethod
    def prepare_domain(cls, name: str, slug: str | None = None) -> str:
        value = slug or name

        prepared_slug = cls.normalize_domain(value)

        if not prepared_slug:
            prepared_slug = "tenant"

        return cls.ensure_domain_not_reserved(prepared_slug)

    @classmethod
    def generate_unique_schema(cls, base: str) -> str:
        base_slug = cls.prepare_schema(name=base)

        slug = base_slug
        counter = 1

        while Tenant.objects.filter(slug=slug).exists():
            slug = f"{base_slug}_{counter}"
            counter += 1

        return slug

    @classmethod
    def prepare(cls, name: str, slug: str | None = None) -> str:
        return cls.prepare_schema(
            name=name,
            slug=slug,
        )
