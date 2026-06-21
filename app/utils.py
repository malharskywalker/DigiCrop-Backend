import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "plot_sensor_data.json"


def ensure_data_file_exists() -> None:
    """
    Make sure the data directory and JSON file exist.
    If not, create them with an empty timeseries structure.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"timeseries": []}, f, indent=2)


def read_data() -> dict:
    """
    Read the JSON file and return its content as a dict.
    """
    ensure_data_file_exists()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_data(data: dict) -> None:
    """
    Safely overwrite the JSON file:
    1. Write to a temporary file
    2. Replace the original file atomically
    """
    ensure_data_file_exists()

    temp_file = DATA_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    os.replace(temp_file, DATA_FILE)