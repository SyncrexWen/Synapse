import yaml
from typing import Dict, Any
from pathlib import Path

DEFAULT_CONFIG: Dict[str, Any] = {
    "initialized": True,
    "app": {
        "log_path": "/logs/app.log",
        "log_level": "INFO"
    }
}

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"

def init_config_file():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            yaml.safe_dump(DEFAULT_CONFIG, f)

def config_read() -> Dict[str, Any]:
    init_config_file()
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def config_dump(data: Dict[str, Any]):
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(data, f)