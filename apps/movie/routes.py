from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination, paginate

from apps.movie.models import Movie
from apps.movie.schema import MovieSchema

router = APIRouter()


@router.get("/")
async def get_movie_all() -> Page[MovieSchema]:
    movie_all = await Movie.all().values()
    return paginate(movie_all)


add_pagination(router)