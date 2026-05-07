from pathlib import Path
from datetime import datetime

CAPTURE_DIR = Path("captures")
CAPTURE_DIR.mkdir(exist_ok=True)

def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return CAPTURE_DIR / f"{timestamp}.jpg"