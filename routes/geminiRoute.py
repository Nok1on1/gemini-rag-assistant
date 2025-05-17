from fastapi import APIRouter, Query, Depends
from controllers.geminiController import (
    LoadData,
    ragData,
    query_data,
    UserInput,
    get_history,
)
from utils.databaseUtils import is_admin_dependency
from typing import List

router = APIRouter()


@router.post("/loadRagData")
async def load_data_endpoint(
    ragData: List[ragData], user_id=Depends(is_admin_dependency)
):
    return LoadData(ragData)


@router.put("/extractRagData")
async def extract_information_endpoint(rag_data_list: UserInput):
    result = await query_data(rag_data_list)
    return {"retrieved_data": result[1], "answer": result[0]}  # type: ignore


@router.get("/getHistory")
async def get_history_endpoint(user_id: str = Query(...)):
    return await get_history(user_id)
