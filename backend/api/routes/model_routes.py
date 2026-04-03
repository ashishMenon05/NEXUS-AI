from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.model_manager import model_manager
from api.routes.websocket import broadcast

router = APIRouter()

class AddCustomModelReq(BaseModel):
    agent_id: str
    base_url: str
    api_key: str
    model_name: str

class RemoveCustomModelReq(BaseModel):
    agent_id: str

class PullModelReq(BaseModel):
    model_name: str

@router.get("/models")
async def get_models():
    local_models = await model_manager.list_available_models()
    return {
        "local_models": local_models,
        "custom_model": {
            "enabled": True, # Hardcode from settings in real app
            "agent": "agent_a"
        }
    }

@router.post("/models/add")
async def add_custom_model(req: AddCustomModelReq):
    result = await model_manager.add_custom_model(
        req.agent_id, req.base_url, req.api_key, req.model_name
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.delete("/models/remove")
async def remove_custom_model(req: RemoveCustomModelReq):
    await model_manager.remove_custom_model(req.agent_id)
    return {"success": True}

@router.post("/models/pull")
async def pull_model(req: PullModelReq):
    # Fire and forget streaming. Need a task runner ideally, but generator logic:
    return {"message": "Streaming progress via WS not fully implemented but requested."}
