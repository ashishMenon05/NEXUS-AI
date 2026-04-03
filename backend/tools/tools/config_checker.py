from pydantic import BaseModel

class CheckConfigParams(BaseModel):
    service: str
    parameter: str

def tool_check_config(params: dict, scenario: dict, round_num: int) -> str:
    service = params.get("service", "").lower()
    parameter = params.get("parameter", "").lower()
    key = f"check_config:{service}:{parameter}"
    
    clue_map = scenario.get("clue_map", {})
    
    # Try exact match
    if key in clue_map:
        return clue_map[key]
        
    # Try partial match (just service)
    service_key = f"check_config:{service}"
    if service_key in clue_map:
        return clue_map[service_key]
        
    # Partial fallback logic for searching parameters in keys
    for k, v in clue_map.items():
        if k.startswith(f"check_config:{service}:") and parameter in k:
            return v

    return f"Configuration for '{parameter}' on '{service}' shows standard default values."
