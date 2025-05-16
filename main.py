from typing import Union
from fastapi import FastAPI
from routes.geminiRoute import router as gemini_router
from routes.authRoute import router as auth_router
from middlewares.deserializeUser import AuthMiddleware

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.add_middleware(AuthMiddleware)

app.include_router(gemini_router, prefix="/gemini", tags=["Gemini"])
