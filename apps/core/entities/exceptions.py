from ninja.errors import HttpError

# ================================================================
# Entity Errors
# ================================================================

class EntityError(HttpError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(status_code=status_code, message=message)

class EntityNotFoundError(EntityError):
    def __init__(self, entity_id: int):
        message = f"Entity with ID '{entity_id}' not found."
        super().__init__(message=message, status_code=404)

        
# ================================================================
# EntityType Errors
# ================================================================
class EntityTypeAlreadyExistsError(EntityError):
    def __init__(self, code: str):
        message = f"EntityType with code '{code}' already exists."
        super().__init__(message=message, status_code=400)


# ================================================================
# Entity Errors
# ================================================================
class EntityNotFoundError(EntityError):
    def __init__(self, entity_id: int):
        message = f"Entity with ID '{entity_id}' not found."
        super().__init__(message=message, status_code=404)


# ================================================================
# RelationType Errors
# ================================================================

class RelationTypeAlreadyExistsError(EntityError):
    def __init__(self, code: str):
        message = f"RelationType with code '{code}' already exists."
        super().__init__(message=message, status_code=400)

# ================================================================
# EntityRelation Errors
# ================================================================

class EntityRelationAlreadyExistsError(EntityError):
    def __init__(self, entity1_id: int, entity2_id: int, relation_type_code: str):
        message = (
            f"EntityRelation between Entity '{entity1_id}' and Entity '{entity2_id}' "
            f"with RelationType '{relation_type_code}' already exists."
        )
        super().__init__(message=message, status_code=400)

