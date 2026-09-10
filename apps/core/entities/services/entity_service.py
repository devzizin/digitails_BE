from django.db import transaction

from apps.core.entities.models import (
    Entity,
    EntityRelation,
    EntityType,
    RelationType,
)
from apps.core.entities.exceptions import (
    EntityTypeAlreadyExistsError,
    EntityNotFoundError,
    RelationTypeAlreadyExistsError,
    EntityRelationAlreadyExistsError,
)


class EntityTypeService:
    @staticmethod
    @transaction.atomic
    def create_entity_type(
        *,
        code: str,
        module_code: str,
        label: str,
        description: str | None = None,
        is_system: bool = False,
    ) -> EntityType:
        if EntityType.objects.filter(code=code).exists():
            raise EntityTypeAlreadyExistsError(code)

        return EntityType.objects.create(
            code=code,
            module_code=module_code,
            label=label,
            description=description,
            is_system=is_system,
        )

    @staticmethod
    @transaction.atomic
    def register_entity_type(
        *,
        code: str,
        module_code: str,
        label: str,
        description: str | None = None,
        is_system: bool = False,
    ) -> EntityType:
        entity_type = EntityType.objects.filter(code=code).first()
        if entity_type is not None:
            return entity_type

        return EntityType.objects.create(
            code=code,
            module_code=module_code,
            label=label,
            description=description,
            is_system=is_system,
        )

    @staticmethod
    @transaction.atomic
    def update_entity_type(
        *,
        entity_type: EntityType,
        label: str,
        description: str | None = None,
    ) -> EntityType:
        entity_type.label = label
        entity_type.description = description
        entity_type.save(update_fields=["label", "description", "updated_at"])
        return entity_type



class EntityService:

    @staticmethod
    @transaction.atomic
    def create_entity(*, entity_type: EntityType, code: str) -> Entity:
        return Entity.objects.create(entity_type=entity_type, code=code)

    @staticmethod
    @transaction.atomic
    def update_entity(*, entity: Entity, entity_type: EntityType, code: str) -> Entity:
        entity.entity_type = entity_type
        entity.code = code
        entity.save(update_fields=["entity_type", "code", "updated_at"])
        return entity

class RelationTypeService:
    @staticmethod
    @transaction.atomic
    def create_relation_type(*, code: str, description: str | None = None) -> RelationType:
        if RelationType.objects.filter(code=code).exists():
            raise RelationTypeAlreadyExistsError(code)

        return RelationType.objects.create(code=code, description=description)


class EntityRelationService:
    @staticmethod
    @transaction.atomic
    def create_entity_relation(
        *,
        source: Entity,
        target: Entity,
        relation_type: RelationType,
    ) -> EntityRelation:
        if EntityRelation.objects.filter(
            source=source, target=target, relation_type=relation_type
        ).exists():
            raise EntityRelationAlreadyExistsError(
                source_id=source.id,
                target_id=target.id,
                relation_type_code=relation_type.code,
            )

        return EntityRelation.objects.create(
            source=source, target=target, relation_type=relation_type
        )

    def update_entity_relation(
        *,
        entity_relation: EntityRelation,
        source: Entity,
        target: Entity,
        relation_type: RelationType,
    ) -> EntityRelation:
        entity_relation.source = source
        entity_relation.target = target
        entity_relation.relation_type = relation_type
        entity_relation.save(update_fields=["source", "target", "relation_type", "updated_at"])
        return entity_relation

