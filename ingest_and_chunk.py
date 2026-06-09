"""
Milestone 3: Document Ingestion and Chunking
Domain: BU CS Professor Reviews
Chunk size: 500 characters | Overlap: 100 characters
"""

import os
import json


# ─────────────────────────────────────────────
# STEP 1: Load documents from the /documents folder
# ─────────────────────────────────────────────

def load_documents(docs_dir="documents"):
    """
    Loads all .txt files from the given directory.
    Returns a list of dicts: {source, text}
    """
    documents = []
    if not os.path.exists(docs_dir):
        print(f"[ERROR] '{docs_dir}' folder not found. Create it and add your .txt files.")
        return documents

    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            documents.append({
                "source": filename,
                "text": raw_text
            })
            print(f"[LOADED] {filename} ({len(raw_text)} chars)")

    print(f"\nTotal documents loaded: {len(documents)}\n")
    return documents


# ─────────────────────────────────────────────
# STEP 2: Clean each document
# ─────────────────────────────────────────────

import re

def clean_text(text):
    """
    Removes HTML tags, common boilerplate, and normalizes whitespace.
    Keeps review content, professor names, and opinions.
    """
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode common HTML entities
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&#39;", "'")
    text = text.replace("&quot;", '"')

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove Reddit/forum boilerplate patterns
    boilerplate_patterns = [
        r"Posted by u/\S+",
        r"\d+ (comments?|upvotes?|points?|awards?)",
        r"Share\s+Save\s+Hide\s+Report",
        r"(Reply|Share|Report|Save|Follow)",
        r"level \d+",
        r"Continue this thread",
        r"more repl(y|ies)",
        r"View entire discussion.*",
        r"Posted \d+.*ago",
        r"cookies? (and|&) (similar )?technolog(y|ies)",
        r"Read more",
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ─────────────────────────────────────────────
# STEP 3: Chunk text
# ─────────────────────────────────────────────

def chunk_text(text, source, chunk_size=500, overlap=100):
    """
    Splits text into overlapping character-level chunks.
    Each chunk includes metadata: source and chunk index.
    Returns a list of dicts: {source, chunk_index, text}
    """
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append({
                "source": source,
                "chunk_index": chunk_index,
                "text": chunk
            })
            chunk_index += 1

        start += chunk_size - overlap  # advance by (chunk_size - overlap)

    return chunks


# ─────────────────────────────────────────────
# STEP 4: Run the full pipeline
# ─────────────────────────────────────────────

def run_pipeline(docs_dir="documents", output_file="chunks.json"):
    documents = load_documents(docs_dir)

    if not documents:
        print("No documents found. Exiting.")
        return

    all_chunks = []

    for doc in documents:
        cleaned = clean_text(doc["text"])

        # Print one document for manual inspection
        if doc == documents[0]:
            print("=" * 60)
            print(f"CLEANED SAMPLE — {doc['source']}:")
            print(cleaned[:800])
            print("=" * 60 + "\n")

        chunks = chunk_text(cleaned, source=doc["source"])
        all_chunks.extend(chunks)

    print(f"Total chunks produced: {len(all_chunks)}")

    # ─────────────────────────────────────────────
    # STEP 5: Inspect 5 sample chunks
    # ─────────────────────────────────────────────
    import random
    print("\n--- 5 RANDOM SAMPLE CHUNKS ---")
    sample = random.sample(all_chunks, min(5, len(all_chunks)))
    for i, chunk in enumerate(sample):
        print(f"\n[Chunk {i+1}] Source: {chunk['source']} | Index: {chunk['chunk_index']}")
        print(chunk["text"])
        print("-" * 40)

    # ─────────────────────────────────────────────
    # STEP 6: Save chunks to JSON for next milestone
    # ─────────────────────────────────────────────
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\n[SAVED] {len(all_chunks)} chunks → {output_file}")

    # Warn if chunk count is outside expected range
    if len(all_chunks) < 50:
        print("[WARNING] Fewer than 50 chunks — consider smaller chunk size or adding more documents.")
    elif len(all_chunks) > 2000:
        print("[WARNING] More than 2000 chunks — consider larger chunk size.")


if __name__ == "__main__":
    run_pipeline()