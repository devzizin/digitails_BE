from ninja import Schema

class EntityResponse(Schema):
    uuid: str
    code: str
    entity_type: str
    description: str | None = None