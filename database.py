"""
Access-control storage layer.

Stores the set of Telegram user IDs who are allowed to use the bot's
work commands (drm/doc/y2t/ytm/t2t/e2t/title/cookies/stop/reset/logs),
plus a list of chat IDs the owner has broadcast to before (so /broadusers
has something to show).

Uses MongoDB via motor (already an existing dependency in requirements.txt).
If MONGO_URI is not set, the bot still runs, but only the OWNER_ID will be
treated as authorized (no persistence across restarts for anyone else).
"""

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB_NAME, OWNER_ID

_client = None
_db = None

if MONGO_URI:
    _client = AsyncIOMotorClient(MONGO_URI)
    _db = _client[MONGO_DB_NAME]
    _authorized_col = _db["authorized_users"]
    _broadcast_col = _db["broadcast_users"]
else:
    _authorized_col = None
    _broadcast_col = None


async def add_authorized_user(user_id: int):
    if _authorized_col is None:
        return False
    await _authorized_col.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True,
    )
    return True


async def remove_authorized_user(user_id: int):
    if _authorized_col is None:
        return False
    result = await _authorized_col.delete_one({"user_id": user_id})
    return result.deleted_count > 0


async def get_authorized_users():
    if _authorized_col is None:
        return []
    cursor = _authorized_col.find({})
    return [doc["user_id"] async for doc in cursor]


async def is_authorized(user_id: int) -> bool:
    if user_id == OWNER_ID and OWNER_ID != 0:
        return True
    if _authorized_col is None:
        return False
    doc = await _authorized_col.find_one({"user_id": user_id})
    return doc is not None


async def record_broadcast_user(chat_id: int):
    """Remember a chat that has interacted with the bot, so /broadcast can reach it."""
    if _broadcast_col is None:
        return
    await _broadcast_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )


async def get_broadcast_users():
    if _broadcast_col is None:
        return []
    cursor = _broadcast_col.find({})
    return [doc["chat_id"] async for doc in cursor]
