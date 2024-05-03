from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination, paginate

from apps.user.models import User
from apps.user.schema import UserSchema

router = APIRouter()


@router.get("/")
async def get_user_all() -> Page[UserSchema]:
    user_all = await User.all().values()
    return paginate(user_all)


add_pagination(router)