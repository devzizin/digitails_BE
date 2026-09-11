import uuid

from ninja import Router

from apps.core.entities.selectors.entity_selector import EntitySelector
from apps.core.entities.services.entity_service import EntityService
from apps.core.entities.exceptions import (
    EntityTypeAlreadyExistsError,
    EntityNotFoundError,
    RelationTypeAlreadyExistsError,
    EntityRelationAlreadyExistsError,
)
from apps.core.entities.api.schemas import (
    EntityResponse,
)


router = Router(tags=["Entities"])

@router.get("/entities", response=list[EntityResponse])
def list_entities(entity_type_code: str | None = None):
    """
    List entities, optionally filtered by entity type code.
    """
    return EntitySelector.list_entities(entity_type_code=entity_type_code)


@router.get("/entities/{entity_uuid}", response=EntityResponse)
def get_entity(entity_uuid: uuid.UUID):
    """
    Get an entity by its UUID.
    """
    try:
        return EntitySelector.get_entity_by_id(entity_uuid)
    except EntityNotFoundError as e:
        return {"error": str(e)}, 404   