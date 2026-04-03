from pydantic import BaseModel

class ReadLogsParams(BaseModel):
    service: str
    time_range: str = "last_24h"

def tool_read_logs(params: dict, scenario: dict, round_num: int) -> str:
    service = params.get("service", "").lower()
    key = f"read_logs:{service}"
    
    clue_map = scenario.get("clue_map", {})
    if key in clue_map:
        return clue_map[key]
    
    return f"No anomalies found in logs for service: {service}."
