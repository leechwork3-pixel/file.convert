from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.botdb
users = db.users
files = db.files

async def log_user(user):
    await users.update_one(
        {"_id": user.id},
        {"$setOnInsert": {
            "name": user.first_name, "username": user.username, "banned": False
        }},
        upsert=True
    )

async def is_banned(user_id):
    doc = await users.find_one({"_id": user_id})
    return doc and doc.get("banned", False)

async def ban_user(user_id):
    await users.update_one({"_id": user_id}, {"$set": {"banned": True}})

async def unban_user(user_id):
    await users.update_one({"_id": user_id}, {"$set": {"banned": False}})

async def log_file(user_id, file_name, fmt):
    await files.insert_one({"user_id": user_id, "file_name": file_name, "format": fmt})

async def get_total_users():
    return await users.count_documents({})

async def get_total_files():
    return await files.count_documents({})

async def get_recent_users(limit=5):
    return await users.find().sort("_id", -1).to_list(length=limit)

async def get_recent_files(limit=5):
    return await files.find().sort("_id", -1).to_list(length=limit)

