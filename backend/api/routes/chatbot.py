from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.app import app
from typing import Dict
from core.auth import get_current_user
from rag.memorystore import MemoryStore

class ChatRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/chatbot")
def chatbot(request: ChatRequest, current_user: Dict = Depends(get_current_user)):
    pipeline = app.state.router_pipeline
    session_id = current_user["username"]
    role = current_user["role"]

    result = pipeline.run(request.query, role, session_id)

    return {
        "message": result["result"],
        "mode": result["mode"],
        "status": result["status"]
    }

@router.post("/clear_memory")
def clear_memory(current_user: dict = Depends(get_current_user)):
    session_id = current_user["username"]
    memorystore: MemoryStore = app.state.memory_store
    memorystore.reset_memory(session_id)
    return {"message": "Memory cleared successfully."}
