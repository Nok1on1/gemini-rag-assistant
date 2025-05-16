from fastapi import APIRouter, Depends, Response
from controllers.authController import sign_in, SignInData
from typing import List

router = APIRouter()


@router.post("/signIn")
async def sign_in_endpoint(response: Response, data: SignInData):
    return sign_in(data, response)
