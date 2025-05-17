from fastapi import HTTPException, status, Query
from bson.objectid import ObjectId
from langchain.schema import AIMessage, HumanMessage
from pymongo import AsyncMongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncMongoClient(os.getenv("MONGO_CONNECTION_STRING"))
users_collection_name = "users"
users_collection = client["Gragnily"][users_collection_name]


def convert_mongo_history_to_langchain(history_data):
    messages = []
    for item in history_data:
        role = item.get("role")
        text = item.get("parts", [{}])[0].get("text", "")

        if role == "user":
            messages.append(HumanMessage(content=text))
        elif role == "model":
            messages.append(AIMessage(content=text))
    return messages


def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    return obj


async def is_admin_dependency(user_id: str = Query(...)):

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user ID"
        )

    try:
        object_id = ObjectId(user_id)
        user = await users_collection.find_one({"_id": object_id})
        if user and user.get("isVerified") and user.get("role") == "admin":
            return user  # You can return just True if you don't need the user object
    except Exception:
        pass

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
