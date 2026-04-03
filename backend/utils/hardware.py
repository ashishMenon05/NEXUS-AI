import subprocess
import re

def check_hardware() -> dict:
    # Auto-detect available VRAM via subprocess nvidia-smi call
    vram_available_mb = 0
    use_gpu = False
    
    try:
        # Run nvidia-smi to get free memory
        # Format: memory.free [MiB]
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.free', '--format=csv,noheader,nounits'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if lines and lines[0].isdigit():
                vram_available_mb = int(lines[0])
                use_gpu = True
    except FileNotFoundError:
        pass
    except Exception:
        pass
        
    vram_available_gb = vram_available_mb / 1024.0
    
    # If VRAM < 3GB available, set num_gpu=0 in Ollama
    if use_gpu and vram_available_gb < 3.0:
        use_gpu = False
        
    return {
        "vram_available_gb": round(vram_available_gb, 2),
        "use_gpu": use_gpu
    }
