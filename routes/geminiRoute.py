from fastapi import APIRouter, Depends, Request
from controllers.geminiController import (
    LoadData,
    ragData,
    query_data,
    UserInput,
    get_history,
)
from typing import List

router = APIRouter()


@router.post("/loadRagData")
async def load_data_endpoint(rag_data_list: List[ragData]):
    return LoadData(rag_data_list)


@router.put("/extractRagData")
async def extract_information_endpoint(rag_data_list: UserInput, request: Request):
    result = await query_data(rag_data_list, request)
    return {"Retrieved Data": result[1], "Answer": result[0]} # type: ignore


@router.get("/getHistory")
async def get_history_endpoint(request: Request):
    return await get_history(request)
