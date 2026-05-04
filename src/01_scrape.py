import requests
import os
import time

START_YEAR = 1991
END_YEAR   = 2024
RAW_DIR    = "data/raw/"
BASE_URL   = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master"

os.makedirs(RAW_DIR, exist_ok=True)

for year in range(START_YEAR, END_YEAR + 1):
    filename = f"atp_matches_{year}.csv"
    url      = f"{BASE_URL}/{filename}"
    out_path = os.path.join(RAW_DIR, filename)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(out_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {filename}")
        time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")
