import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from apps.docs import routes as docs_router
from apps.auth.middlewares import AuthMiddleware
from apps.docs.custom_openai import custom_openapi
from apps.user import routes as user_router
from apps.movie import routes as movie_router

load_dotenv()


def init_db(instance: FastAPI) -> None:
    register_tortoise(
        instance,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["apps.user.models", "apps.movie.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def create_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(AuthMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=[
            "DELETE",
            "GET",
            "OPTIONS",
            "PATCH",
            "POST",
            "PUT",
        ],
        allow_headers=["*"]
    )

    application.include_router(docs_router.router, tags=['user'])
    application.include_router(user_router.router, prefix="/user", tags=['user'])
    application.include_router(movie_router.router, prefix="/movie", tags=['movie'])

    return application


app = create_application()

app.openapi = lambda: custom_openapi(app)


@app.on_event('startup')
async def startup_event():
    init_db(app)
