import uuid
from pathlib import Path
from typing import Tuple

def generate_uuid(file_path: str) -> Tuple[int, str]:
    '''Generate a random UUID string'''
    path = Path(file_path)
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    # Extract file name
    file_name = path.stem
    # Generate random UUID
    unique_id = uuid.uuid4()

    return unique_id.int, file_name
