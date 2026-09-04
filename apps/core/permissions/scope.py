from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from apps.core.entities.public.scope import entity_scope_graph

if TYPE_CHECKING:
    from apps.core.entities.models import Entity
    from apps.core.entities.public.scope import EntityScopeGraph


class PermissionScopeUsageError(ValueError):
    """PermissionScope was combined with an incompatible legacy scope."""


@dataclass(frozen=True, slots=True)
class PermissionScope:
    """An explicit Entity anchor for a permission decision."""

    scope_entity: Entity

    def resolve_entities(
        self,
        *,
        graph: EntityScopeGraph | None = None,
    ) -> list[Entity]:
        resolver = graph or entity_scope_graph
        return resolver.resolve(self.scope_entity)
