from typing import Union
from fastapi import FastAPI
from routes.geminiRoute import router as gemini_router
from routes.authRoute import router as auth_router
from middlewares.deserializeUser import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "https://gragnily.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.add_middleware(AuthMiddleware)

app.include_router(gemini_router, prefix="/gemini", tags=["Gemini"])
