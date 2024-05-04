import uuid

from tortoise import fields, Model


class ListJSONField(fields.JSONField):
    def to_db_value(self, value, instance):
        if not isinstance(value, list):
            raise ValueError("Value must be a list")
        return super().to_db_value(value, instance)


class Movie(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=255)
    tags = ListJSONField()