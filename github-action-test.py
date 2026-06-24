import requests
import json
import pandas as pd
from datetime import datetime

LOG_FILE = "etl_log.txt"

try:
    response = requests.get("https://api.datausa.io/tesseract/cubes")
    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict) and "cubes" in data:
        df = pd.DataFrame(data["cubes"])

        row_count = len(df)

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        log_message = (
            f"{timestamp} | API call successful | "
            f"Rows fetched: {row_count}\n"
        )

        with open(LOG_FILE, "a") as f:
            f.write(log_message)

        print(log_message)

    else:
        raise ValueError("Unexpected API response structure")

except Exception as e:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    error_message = (
        f"{timestamp} | API call failed | Error: {str(e)}\n"
    )

    with open(LOG_FILE, "a") as f:
        f.write(error_message)

    print(error_message)