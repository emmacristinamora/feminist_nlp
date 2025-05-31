import os
import time
import logging
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

# === BASE REPO PATH === #
REPO_DIR = Path(__file__).resolve().parents[1]
BOOK_LINKS_PATH = REPO_DIR / "data" / "book_links.csv"
RAW_DIR = REPO_DIR / "data" / "raw"
METADATA_PATH = REPO_DIR / "data" / "metadata.csv"
LOG_DIR = REPO_DIR / "logs"
LOG_FILE = LOG_DIR / "extract_books.log"

# set up logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_books():
    logging.info("Starting book extraction process...")

    # create raw data directory if it doesn't exist
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # load book links
    df = pd.read_csv(BOOK_LINKS_PATH)

    # metadata storage
    metadata = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        title = row["title"]
        url = row["url"]
        filename = f"{re.sub(r'[^a-zA-Z0-9_]', '', title.replace(' ', '_'))}.txt"
        filepath = RAW_DIR / filename

        # skip if file already exists
        if filepath.exists():
            logging.info(f"Skipping {title}, already downloaded.")
        else:
            for attempt in range(3):
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    logging.info(f"Downloaded {title} successfully.")
                    break
                except Exception as e:
                    logging.warning(f"Attempt {attempt + 1} failed for {title}: {e}")
                    time.sleep(2)
            else:
                logging.error(f"Failed to download {title} after 3 attempts.")
                continue

        # author extraction
        inferred_author = row["author"]

        # year extraction
        year = row["date"]

        metadata.append({
            "id": filename.replace('.txt', ''),  # or generate a UUID
            "title": title,
            "author": inferred_author,
            "filename": filename,
            "year": year,
        })

    # save metadata
    metadata_df = pd.DataFrame(metadata)
    metadata_df.to_csv(METADATA_PATH, index=False)
    logging.info(f"Metadata saved to {METADATA_PATH}")

if __name__ == "__main__":
    extract_books()