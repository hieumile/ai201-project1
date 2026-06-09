"""
Milestone 4: Embedding and Retrieval
- Loads chunks from chunks.json
- Embeds with all-MiniLM-L6-v2
- Stores in ChromaDB with source metadata
- Retrieval function with top-k=5
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer

# ─────────────────────────────────────────────
# STEP 1: Load chunks from Milestone 3 output
# ─────────────────────────────────────────────

def load_chunks(filepath="chunks.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"[LOADED] {len(chunks)} chunks from {filepath}")
    return chunks


# ─────────────────────────────────────────────
# STEP 2: Set up embedding model and ChromaDB
# ─────────────────────────────────────────────

def build_vector_store(chunks, collection_name="bu_cs_reviews"):
    # Load embedding model (runs locally, no API key needed)
    print("[EMBEDDING] Loading all-MiniLM-L6-v2...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB (persisted to disk so you don't re-embed every run)
    client = chromadb.PersistentClient(path="./chroma_db")

    # Delete existing collection if it exists (clean rebuild)
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(collection_name)

    # Embed all chunks
    texts = [chunk["text"] for chunk in chunks]
    print(f"[EMBEDDING] Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Store in ChromaDB with metadata
    collection.add(
        ids=[f"{chunk['source']}__chunk{chunk['chunk_index']}" for chunk in chunks],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in chunks
        ]
    )

    print(f"[STORED] {len(chunks)} chunks in ChromaDB collection '{collection_name}'\n")
    return model, collection


# ─────────────────────────────────────────────
# STEP 3: Retrieval function
# ─────────────────────────────────────────────

def retrieve(query, model, collection, top_k=5):
    """
    Embeds the query and returns the top-k most relevant chunks
    with their text, source, and distance score.
    """
    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks_out = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks_out.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4)
        })

    return chunks_out


# ─────────────────────────────────────────────
# STEP 4: Test retrieval with evaluation queries
# ─────────────────────────────────────────────

TEST_QUERIES = [
    "What do students say about David Sullivan's teaching style?",
    "What opinions do students have about Christine Papadakis-Kanaris (CPK) for CS112?",
    "What opinions do students have about Mark Crovella?",
]

def test_retrieval(model, collection):
    for query in TEST_QUERIES:
        print("=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)
        results = retrieve(query, model, collection, top_k=5)
        for i, r in enumerate(results):
            print(f"\n  [Result {i+1}] Source: {r['source']} | Distance: {r['distance']}")
            print(f"  {r['text'][:300]}")
        print()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    chunks = load_chunks("chunks.json")
    model, collection = build_vector_store(chunks)
    test_retrieval(model, collection)
    print("[DONE] Retrieval test complete. Review results above before moving to Milestone 5.")