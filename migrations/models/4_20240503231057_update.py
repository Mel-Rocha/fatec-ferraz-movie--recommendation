from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "movie" ALTER COLUMN "tags" TYPE TEXT USING "tags"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "movie" ALTER COLUMN "tags" TYPE JSONB USING "tags"::JSONB;"""
