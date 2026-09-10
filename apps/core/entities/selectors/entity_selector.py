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


class EntitySelector:


    @staticmethod
    def list_entities(*, entity_type_code: str | None = None) -> list[Entity]:
        """
        List entities, optionally filtered by entity type code.
        """
        query = Entity.objects.all()
        if entity_type_code:
            query = query.filter(entity_type__code=entity_type_code)
        return list(query)
    

    @staticmethod
    def get_entity_by_id(entity_uuid: int) -> Entity:
        entity = Entity.objects.filter(uuid=entity_uuid).first()
        if entity is None:
            raise EntityNotFoundError(entity_uuid)
        return entity

    @staticmethod
    def get_entity_by_code(code: str) -> Entity:
        entity = Entity.objects.filter(code=code).first()
        if entity is None:
            raise EntityNotFoundError(code)
        return entity

