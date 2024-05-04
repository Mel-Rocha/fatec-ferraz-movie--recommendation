from typing import Dict

import pandas as pd
from fastapi import APIRouter
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from fastapi_pagination import Page, add_pagination, paginate

from apps.movie.models import Movie
from apps.movie.schema import MovieSchema

router = APIRouter()


@router.get("/")
async def get_movie_all() -> Page[MovieSchema]:
    movie_all = await Movie.all().values()
    return paginate(movie_all)


add_pagination(router)


@router.get("/calculate/similarity/{movie1_name}/{movie2_name}")
async def calculate_similarity(movie1_name: str, movie2_name: str):
    try:
        movie1 = await Movie.get(title=movie1_name)
        movie2 = await Movie.get(title=movie2_name)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found")

    similarity = 0
    similarity += (movie1.genre == movie2.genre)
    similarity += len(set(movie1.tags).intersection(set(movie2.tags)))

    return {"similarity": similarity}