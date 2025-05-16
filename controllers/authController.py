from fastapi import Request, Response
from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt
import jwt

load_dotenv()

client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

dbName = "Gragnily"

users_collection_name = "users"
users_collection = client[dbName][users_collection_name]


class SignInData(BaseModel):
    username: str
    password: str


def sign_in(data: SignInData, response: Response):
    username = data.username
    password = data.password.encode("utf-8")
    try:
        found_user = users_collection.find_one({"username": username})

        if found_user is None:
            return {"error": "User not found"}
        elif not found_user.get("isVerified", False):
            return {"error": "User not verified"}

        hashed = found_user["password"]
        if isinstance(hashed, str):
            hashed = hashed.encode("utf-8")

        passwordIsValid = bcrypt.checkpw(password, hashed)
        if not passwordIsValid:
            return {"error": "Invalid password"}

        access_token = jwt.encode({"user_id": str(found_user["_id"])}, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")  # type: ignore
        refresh_token = jwt.encode({"user_id": str(found_user["_id"])}, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")  # type: ignore

        response.set_cookie(
            key="x-access-token",
            value=access_token,
            max_age=20000,
            httponly=True,
            samesite="none" if os.getenv("ENV") == "production" else "lax",
            secure=os.getenv("ENV") == "production",
        )
        response.set_cookie(
            key="x-refresh-token",
            value=refresh_token,
            max_age=86400000,
            httponly=True,
            samesite="none" if os.getenv("ENV") == "production" else "lax",
            secure=os.getenv("ENV") == "production",
        )
    except Exception as e:
        return {"error": str(e)}

    return {"success": "Login successful"}
