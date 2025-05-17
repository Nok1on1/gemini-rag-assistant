from fastapi import APIRouter, Query
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
async def extract_information_endpoint(rag_data_list: UserInput):
    result = query_data(rag_data_list)
    return {"retrieved_data": result[1], "answer": result[0]}  # type: ignore


@router.get("/getHistory")
async def get_history_endpoint(user_id: str = Query(...)):
    return await get_history(user_id)
