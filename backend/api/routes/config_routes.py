from fastapi import APIRouter
from config import settings
from pydantic import BaseModel
from utils.hardware import check_hardware

router = APIRouter()

class ConfigUpdate(BaseModel):
    MAX_STEPS: int
    AGENT_A_MODEL: str
    AGENT_B_MODEL: str
    AGENT_A_PROVIDER: str
    AGENT_B_PROVIDER: str
    AGENT_A_TEMPERATURE: float
    AGENT_B_TEMPERATURE: float

@router.get("/config")
def get_config():
    hw = check_hardware()
    return {
        "models": {
            "agent_a": settings.AGENT_A_MODEL,
            "agent_b": settings.AGENT_B_MODEL,
            "agent_a_provider": settings.AGENT_A_PROVIDER,
            "agent_b_provider": settings.AGENT_B_PROVIDER,
            "agent_a_temp": settings.AGENT_A_TEMPERATURE,
            "agent_b_temp": settings.AGENT_B_TEMPERATURE
        },
        "episode": {
            "max_steps": settings.MAX_STEPS,
            "max_time": settings.MAX_EPISODE_TIME_SECONDS
        },
        "hardware": hw
    }

@router.post("/config")
def update_config(req: ConfigUpdate):
    settings.MAX_STEPS = req.MAX_STEPS
    settings.AGENT_A_MODEL = req.AGENT_A_MODEL
    settings.AGENT_B_MODEL = req.AGENT_B_MODEL
    settings.AGENT_A_PROVIDER = req.AGENT_A_PROVIDER
    settings.AGENT_B_PROVIDER = req.AGENT_B_PROVIDER
    settings.AGENT_A_TEMPERATURE = req.AGENT_A_TEMPERATURE
    settings.AGENT_B_TEMPERATURE = req.AGENT_B_TEMPERATURE
    
    return {"status": "success", "message": "Config updated for next episode"}

@router.post("/pause")
def pause():
    from core.episode_manager import episode_manager
    episode_manager.is_paused = not episode_manager.is_paused
    return {"paused": episode_manager.is_paused}
