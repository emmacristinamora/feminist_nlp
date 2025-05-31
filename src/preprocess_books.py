import os
import re
import spacy
import unicodedata
import textwrap
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# === BASE REPO PATH === #
REPO_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_DIR / "data" / "raw"
PROCESSED_DIR = REPO_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
BOOK_CHUNKS_PATH = PROCESSED_DIR / "processed_book_chunks.csv"
TEXTS_PATH = PROCESSED_DIR / "processed_texts.csv"

# === Load spaCy Transformer Model === #
nlp = spacy.load("en_core_web_trf")

# === Utility Functions === #
def normalize_unicode(text):
    return unicodedata.normalize("NFKC", text)

def strip_gutenberg_boilerplate(text):
    start_re = r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*"
    end_re = r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*"
    start = re.search(start_re, text, re.IGNORECASE)
    end = re.search(end_re, text, re.IGNORECASE)
    if start and end:
        return text[start.end():end.start()].strip()
    return text

def clean_text(text):
    text = normalize_unicode(text)
    text = strip_gutenberg_boilerplate(text)
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_text_chunks(text, chunk_size=200):
    chunks = []
    word_chunks = textwrap.wrap(text, width=chunk_size * 6)  # approx. 6 chars per word
    for chunk_text in word_chunks:
        chunk_text = chunk_text.strip()
        if len(chunk_text) < 100:
            continue

        doc = nlp(chunk_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]

        chunks.append({
            "text": chunk_text,
            "sentiment": None,
            "entities": entities,
            "verbs": verbs
        })
    return chunks

# === Process Books === #
all_chunks = []

for file in tqdm(RAW_DIR.glob("*.txt")):
    title = file.stem.replace("_", " ")
    with open(file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_text = clean_text(raw_text)
    processed_chunks = process_text_chunks(cleaned_text)

    for chunk in processed_chunks:
        chunk["title"] = title
        all_chunks.append(chunk)

# === Save Outputs === #
pd.DataFrame(all_chunks).to_csv(BOOK_CHUNKS_PATH, index=False)
print(f"Saved {BOOK_CHUNKS_PATH.name}")