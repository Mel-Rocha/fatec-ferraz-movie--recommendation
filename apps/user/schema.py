from tortoise.contrib.pydantic import pydantic_model_creator

from apps.user.models import User

UserSchema = None


def initialize_user_schema():
    global UserSchema
    UserSchema = pydantic_model_creator(User)


initialize_user_schema()