#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import shutil

# --- ABSOLUTE PATH ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CSV_TARGET = DATA_DIR / "cost-of-living_v2.csv"
# ---------------------

KAGGLE_DS = "mvieira101/global-cost-of-living"

def main():
    DATA_DIR.mkdir(exist_ok=True)

    print("Downloading dataset from Kaggle...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", KAGGLE_DS,
        "-p", str(DATA_DIR),
        "--unzip", "--force"
    ], check=True)

    # Find the CSV
    csv_files = list(DATA_DIR.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV found after download")

    shutil.move(str(csv_files[0]), str(CSV_TARGET))
    print(f"Dataset ready: {CSV_TARGET}")

if __name__ == "__main__":
    main()