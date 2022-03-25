import motor.motor_asyncio
from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)

db = client[settings.db_name]
users_db = db.users
todo_db = db.todos
