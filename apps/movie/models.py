import uuid

from tortoise import fields, Model


class Movie(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=255)
    tags = fields.JSONField()