from tortoise import Tortoise

from config import Config


async def init():
    await Tortoise.init(
        db_url=Config.DATABASE_URL,
        modules={"models": ["src.models"]}
    )
    await Tortoise.generate_schemas()