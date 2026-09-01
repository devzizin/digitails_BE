import uuid

from django.db import models


class EntityType(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    code = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.TextField(null=True, blank=True)
    is_system = models.BooleanField(
        default=False,
        help_text="Marks platform/system entity types protected from accidental removal.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "entity_types"

    def __str__(self) -> str:
        return self.code


class Entity(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    entity_type = models.ForeignKey(
        EntityType,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "entities"

    def __str__(self) -> str:
        return f"{self.entity_type.code} ({self.id})"

# class RelationType(models.Model):
#     uuid = models.UUIDField(
#         unique=True,
#         default=uuid.uuid4,
#         editable=False,
#         db_index=True,
#     )
#     code = models.CharField(
#         max_length=50,
#         unique=True,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)

class RelationType(models.Choices):
    PARENT_CHILD = "parent_child", "Parent-Child"
    OWNS = "owns", "Owns"
    USES = "uses", "Uses"
    HOSTED_ON = "hosted_on", "Hosted On"
    ASSOCIATED = "associated", "Associated"
    RELATED = "related", "Related"


class EntityRelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    source = models.ForeignKey(
        Entity,
        related_name="outgoing_relations",
        on_delete=models.CASCADE,
    )

    target = models.ForeignKey(
        Entity,
        related_name="incoming_relations",
        on_delete=models.CASCADE,
    )

    type = models.ForeignKey(
        Entity,
        on_delete=models.PROTECT,
    )

    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "entity_relations"
        unique_together = ("source", "target", "type")

    def __str__(self) -> str:
        return f"{self.source} -[{self.type}]-> {self.target}"