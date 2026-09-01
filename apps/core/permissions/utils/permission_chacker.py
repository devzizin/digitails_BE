import logging

from apps.core.permissions.authority import authority_registry
from apps.core.permissions.decision import (
    AuthorizationDecision,
    GrantProvenance,
    GrantSource,
    RejectedGrant,
)
from apps.core.permissions.grant_constraints import (
    GrantConstraintContext,
    GrantConstraintRegistry,
    grant_constraint_registry,
)
from apps.core.permissions.permissions_tenant.models import UserRole
from apps.core.permissions.principals import Principal, PrincipalKind, UserPrincipal
from apps.core.permissions.scope import PermissionScope, PermissionScopeUsageError
from apps.core.permissions.services.platform_admin_service import PlatformAdminService
from apps.core.permissions.validators import PermissionValidators

logger = logging.getLogger(__name__)

_UNSET = object()


class PermissionChecker:
    """
    Evaluates whether a user has a permission
    within a given entity scope.

    Supports:

    - global permissions
    - entity-scoped permissions
    - inherited/cascading scope
    """

    @staticmethod
    def _normalize_principal(
        *,
        user,
        principal: Principal | None,
        is_platform_admin,
    ) -> Principal:
        if user is not None and principal is not None:
            message = "Pass either user= or principal=, not both."
            raise ValueError(message)
        if user is None and principal is None:
            message = "Pass either user= or principal=."
            raise ValueError(message)

        if principal is not None:
            if is_platform_admin is not _UNSET:
                message = (
                    "Do not pass is_platform_admin= with principal=; "
                    "platform-admin state comes from the principal."
                )
                raise ValueError(message)
            if (
                principal.principal_kind != PrincipalKind.USER
                and principal.is_platform_admin
            ):
                message = (
                    "Non-USER principals cannot claim platform-admin status."
                )
                raise ValueError(message)
            return principal

        if is_platform_admin is _UNSET:
            message = "is_platform_admin is required when authorizing with user=."
            raise ValueError(message)
        return UserPrincipal(
            user=user,
            is_platform_admin=is_platform_admin,
        )

    @staticmethod
    def authorize(
        *,
        user=None,
        principal: Principal | None = None,
        permission_code: str,
        is_platform_admin=_UNSET,
        entity=None,
        scope: PermissionScope | None = None,
    ) -> AuthorizationDecision:
        subject = PermissionChecker._normalize_principal(
            user=user,
            principal=principal,
            is_platform_admin=is_platform_admin,
        )

        PermissionValidators.validate_permission_code(
            permission_code,
        )

        scope_entity = None
        if scope is not None:
            if entity is not None:
                message = (
                    "Pass either PermissionScope or the legacy entity list, not both."
                )
                raise PermissionScopeUsageError(message)
            entity = scope.resolve_entities()
            scope_entity = scope.scope_entity

        if subject.is_platform_admin:
            logger.info(
                "PLATFORM ADMIN BYPASS",
            )

            return AuthorizationDecision(
                allowed=True,
                via_platform_admin=True,
            )

        entity_ids = [obj.id for obj in entity]

        logger.info(
            "REQUEST ENTITIES=%s",
            entity_ids,
        )

        grants = authority_registry.get(subject.principal_kind).grants_for(
            principal=subject,
            permission_code=permission_code,
            entity_ids=entity_ids,
        )
        context = GrantConstraintContext(
            principal=subject,
            permission_code=permission_code,
            scope_entity=scope_entity,
            resolved_entities=tuple(entity),
        )
        matched: list[GrantProvenance] = []
        rejected: list[RejectedGrant] = []

        for grant in grants:
            matched_grant, rejected_grant = PermissionChecker._evaluate_grant(
                grant=grant,
                context=context,
            )
            if matched_grant is not None:
                matched.append(matched_grant)
            if rejected_grant is not None:
                rejected.append(rejected_grant)

        decision = AuthorizationDecision(
            allowed=bool(matched),
            matched_grants=tuple(matched),
            rejected_grants=tuple(rejected),
        )

        logger.info(
            "PERMISSION RESULT | principal=%s | permission=%s | entities=%s | result=%s",
            subject.principal_ref,
            permission_code,
            entity_ids,
            decision.allowed,
        )

        return decision

    @staticmethod
    def _evaluate_grant(
        *,
        grant: GrantProvenance,
        context: GrantConstraintContext,
        constraints: GrantConstraintRegistry | None = None,
    ) -> tuple[GrantProvenance | None, RejectedGrant | None]:
        if grant.source == GrantSource.DIRECT:
            if grant.source_id is None:
                return grant, None
            return None, RejectedGrant(
                grant=grant,
                reason="direct grant has a non-null source_id",
            )

        if grant.source_id is None:
            return None, RejectedGrant(
                grant=grant,
                reason=f"{grant.source} grant has no source_id",
            )

        result = (constraints or grant_constraint_registry).evaluate(
            grant=grant,
            context=context,
        )
        if result.allowed:
            return grant, None
        return None, RejectedGrant(
            grant=grant,
            reason=result.reason,
        )

    @staticmethod
    def has_permission(
        *,
        user=None,
        principal: Principal | None = None,
        permission_code: str,
        is_platform_admin=_UNSET,
        entity=None,
        scope: PermissionScope | None = None,
    ) -> bool:
        return PermissionChecker.authorize(
            user=user,
            principal=principal,
            permission_code=permission_code,
            is_platform_admin=is_platform_admin,
            entity=entity,
            scope=scope,
        ).allowed

    @staticmethod
    def is_admin(
        *,
        user,
    ) -> bool:

        if PlatformAdminService.is_platform_admin(
            user,
        ):
            return True

        return UserRole.objects.filter(
            user=user,
            role_template__code__in=[
                "core.company.admin",
                "core.tenant.admin",
            ],
            deleted_at__isnull=True,
        ).exists()
