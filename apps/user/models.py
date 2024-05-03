import uuid

from tortoise import fields, Model


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)