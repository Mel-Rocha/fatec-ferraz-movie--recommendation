import logging

from fastapi import APIRouter
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from fastapi_pagination import Page, add_pagination, paginate

from apps.movie.models import Movie
from apps.movie.schema import MovieSchema
from apps.user.models import User

logging.basicConfig(level=logging.INFO)

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

    return similarity


@router.get("/recommend/{user_id}")
async def recommend_movies(user_id: str):
    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.movies_watched:
        return {"detail": "User has not watched any movies yet"}

    # Obtendo os filmes assistidos pelo usuário do banco de dados
    watched_movies = await Movie.filter(title__in=user.movies_watched).values()
    logging.info(f"Watchde Movies by user: {watched_movies}")

    recommendations = []

    # Calculando a similaridade com cada filme no banco de dados
    for watched_movie in watched_movies:
        for movie in await Movie.all().values():
            if movie['title'] in user.movies_watched:
                logging.info(f"Movie watched BY USER:`{watched_movie} Movie BY DATABASE: {movie}")
                similarity = await calculate_similarity(watched_movie['title'], movie['title'])
                recommendations.append((movie['title'], similarity))
                logging.info(f"similarity {similarity}")

    # Ordenando filmes por maior similaridade
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Retornando os nomes dos filmes mais similares
    return [rec[0] for rec in recommendations[:3]]
