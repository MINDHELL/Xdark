from datetime import datetime, timedelta
from config import *
from database.mongo import super_premium_collection  # create new collection

async def add_super_premium(user_id, time_value, time_unit):
    now = datetime.utcnow()

    if time_unit == "s":
        expiry = now + timedelta(seconds=time_value)
    elif time_unit == "m":
        expiry = now + timedelta(minutes=time_value)
    elif time_unit == "h":
        expiry = now + timedelta(hours=time_value)
    elif time_unit == "d":
        expiry = now + timedelta(days=time_value)
    elif time_unit == "y":
        expiry = now + timedelta(days=365 * time_value)
    else:
        raise ValueError("Invalid time unit")

    await super_premium_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "expiration_timestamp": expiry.isoformat()
        }},
        upsert=True
    )

    return expiry


async def is_super_premium(user_id):
    user = await super_premium_collection.find_one({"user_id": user_id})

    if not user:
        return False

    expiry = datetime.fromisoformat(user["expiration_timestamp"])

    if expiry < datetime.utcnow():
        await super_premium_collection.delete_one({"user_id": user_id})
        return False

    return True
