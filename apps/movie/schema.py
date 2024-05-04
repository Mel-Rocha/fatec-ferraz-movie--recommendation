from tortoise.contrib.pydantic import pydantic_model_creator

from apps.movie.models import Movie

MovieSchema = None


def initialize_movie_schema():
    global MovieSchema
    MovieSchema = pydantic_model_creator(Movie)


initialize_movie_schema()