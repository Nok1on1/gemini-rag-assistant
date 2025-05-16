from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import jwt, os


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            access_token = request.cookies.get("x-access-token")
            refresh_token = request.cookies.get("x-refresh-token")
            user_id = None

            if access_token:
                payload = jwt.decode(access_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])  # type: ignore
                user_id = payload.get("user_id")

            elif refresh_token:
                payload = jwt.decode(refresh_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])  # type: ignore
                user_id = payload.get("user_id")

                # 🔁 Reissue new access token
                new_access_token = jwt.encode(
                    {"user_id": user_id},
                    os.getenv("JWT_SECRET_KEY"),  # type: ignore
                    algorithm="HS256",
                )

                # Save token to set in response later
                request.state.new_access_token = new_access_token

            request.state.user_id = user_id

        except jwt.ExpiredSignatureError:
            request.state.user_id = None

        response = await call_next(request)

        if hasattr(request.state, "new_access_token"):
            response.set_cookie(
                key="x-access-token",
                value=request.state.new_access_token,
                max_age=20000,
                httponly=True,
                samesite="none" if os.getenv("ENV") == "production" else "lax",
                secure=os.getenv("ENV") == "production",
            )

        return response
