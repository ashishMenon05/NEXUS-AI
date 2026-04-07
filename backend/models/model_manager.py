import os
from typing import Tuple, Dict, List
from openai import AsyncOpenAI
import httpx
import json

from config import settings
from .ollama_client import OllamaClient
from .hf_client import HFClient

class ModelManager:
    def __init__(self):
        self.ollama = OllamaClient(settings.OLLAMA_BASE_URL, settings.OLLAMA_API_KEY)
        self.hf = None
        if settings.HF_TOKEN and settings.HF_TOKEN != "your_huggingface_token_here":
            self.hf = HFClient(settings.HF_INFERENCE_URL, settings.HF_TOKEN)
            
    def get_client(self, agent_id: str) -> Tuple[AsyncOpenAI, str]:
        # Check if custom model set for this agent
        if settings.CUSTOM_MODEL_ENABLED:
            if settings.CUSTOM_MODEL_AGENT.lower() == agent_id.lower() or settings.CUSTOM_MODEL_AGENT.lower() == "both":
                client = AsyncOpenAI(
                    base_url=settings.CUSTOM_MODEL_BASE_URL,
                    api_key=settings.CUSTOM_MODEL_API_KEY or "none"
                )
                return client, settings.CUSTOM_MODEL_NAME
                
        # Determine provider and model
        if agent_id == "agent_a":
            provider = settings.AGENT_A_PROVIDER
            model_name = settings.AGENT_A_MODEL
        else:
            provider = settings.AGENT_B_PROVIDER
            model_name = settings.AGENT_B_MODEL
            
        if provider == "hf" and self.hf:
            return self.hf.get_client(), model_name
        elif provider == "openrouter":
            client = AsyncOpenAI(api_key=settings.OPENROUTER_API_KEY, base_url=settings.OPENROUTER_BASE_URL)
            return client, model_name
        elif provider == "openai":
            # We spin up OpenAI dynamically pulling the global OpenAI Key
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            return client, model_name
        
        return self.ollama.get_client(), model_name

    async def add_custom_model(self, agent_id: str, base_url: str, api_key: str, model_name: str) -> dict:
        try:
            # Validate endpoint and test with simple completion
            client = AsyncOpenAI(base_url=base_url, api_key=api_key or "none")
            response = await client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "Say 'hello' in exactly one word."}],
                max_tokens=10,
                timeout=10.0
            )
            
            if response and response.choices:
                # Test passed, update .env file dynamically
                env_map = {
                    "CUSTOM_MODEL_ENABLED": "true",
                    "CUSTOM_MODEL_BASE_URL": base_url,
                    "CUSTOM_MODEL_API_KEY": api_key,
                    "CUSTOM_MODEL_NAME": model_name,
                    "CUSTOM_MODEL_AGENT": agent_id
                }
                self._update_env_file(env_map)
                
                # Update runtime config
                settings.CUSTOM_MODEL_ENABLED = True
                settings.CUSTOM_MODEL_BASE_URL = base_url
                settings.CUSTOM_MODEL_API_KEY = api_key
                settings.CUSTOM_MODEL_NAME = model_name
                settings.CUSTOM_MODEL_AGENT = agent_id
                
                return {"success": True, "message": "Custom model verified and activated."}
            else:
                return {"success": False, "message": "Model did not return a valid completion."}
                
        except Exception as e:
            return {"success": False, "message": f"Validation failed: {str(e)}"}

    async def remove_custom_model(self, agent_id: str):
        if settings.CUSTOM_MODEL_AGENT.lower() == agent_id.lower() or settings.CUSTOM_MODEL_AGENT.lower() == "both":
            env_map = {"CUSTOM_MODEL_ENABLED": "false"}
            self._update_env_file(env_map)
            settings.CUSTOM_MODEL_ENABLED = False

    async def list_available_models(self) -> List[str]:
        return await self.ollama.list_models()

    def pull_model(self, model_name: str):
        return self.ollama.pull_model(model_name)
        
    def _update_env_file(self, overrides: dict):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "default.env")
        if not os.path.exists(env_path):
            return
            
        with open(env_path, "r") as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            updated = False
            for k, v in overrides.items():
                if line.startswith(f"{k}="):
                    new_lines.append(f"{k}={v}\n")
                    updated = True
                    break
            if not updated:
                new_lines.append(line)
                
        with open(env_path, "w") as f:
            f.writelines(new_lines)

model_manager = ModelManager()
