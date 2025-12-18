import re
import random
from langdetect import detect, LangDetectException

# -------------------------------------------------
# 1. Clean extra whitespace
# -------------------------------------------------
def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

# -------------------------------------------------
# 2. Remove special characters
# -------------------------------------------------
def remove_special_characters(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9.,!?;:()'\" \n]", "", text)

# -------------------------------------------------
# 3. Normalize text
# -------------------------------------------------
def normalize_text(text: str) -> str:
    return text.lower()

# -------------------------------------------------
# 4. Remove page numbers / footers
# -------------------------------------------------
def remove_page_numbers(text: str) -> str:
    lines = text.split("\n")
    return "\n".join(
        line for line in lines
        if not re.match(r"^\s*(page\s*)?\d+\s*$", line.lower())
    )

# -------------------------------------------------
# 5. Detect language
# -------------------------------------------------
def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

# -------------------------------------------------
# 6 & 7. Chunk text (non-overlapping)
# -------------------------------------------------
def chunk_text(text: str, min_words=1000, max_words=1500) -> list:
    words = text.split()
    chunks = []
    i = 0

    while i < len(words):
        size = random.randint(min_words, max_words)
        chunk = words[i:i + size]
        chunks.append(" ".join(chunk))
        i += size  # non-overlapping

    return chunks

# -------------------------------------------------
# 8. Full preprocessing pipeline
# -------------------------------------------------
def process_text_pipeline(text: str) -> dict:
    """
    Upload → Extract → Clean → Normalize → Detect → Chunk
    """

    text = clean_whitespace(text)
    text = remove_special_characters(text)
    text = normalize_text(text)
    text = remove_page_numbers(text)

    language = detect_language(text)
    chunks = chunk_text(text)

    return {
        "cleaned_text": text,
        "language": language,
        "chunks": chunks,
        "total_chunks": len(chunks)
    }
