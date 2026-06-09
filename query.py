
import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Load model and vector store (once at startup)
# ─────────────────────────────────────────────

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("bu_cs_reviews")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# ─────────────────────────────────────────────
# Retrieval
# ─────────────────────────────────────────────

def retrieve(query, top_k=5):
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4)
        })
    return chunks


# ─────────────────────────────────────────────
# Grounded Generation
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about BU CS professors 
using only the provided student reviews. 

IMPORTANT RULES:
- Answer ONLY using the information in the provided documents below.
- Do NOT use any outside knowledge or general assumptions about professors or courses.
- If the documents do not contain enough information to answer the question, respond with exactly: 
  "I don't have enough information on that."
- Keep your answer concise and specific, directly referencing what students said.
- Do not make up or infer anything not explicitly stated in the documents."""


def ask(question):
    # Step 1: Retrieve relevant chunks
    chunks = retrieve(question, top_k=5)

    # Step 2: Build context string from chunks
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"[Document {i+1} — {chunk['source']}]\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    # Step 3: Build prompt
    user_prompt = f"""Documents:
{context}

Question: {question}

Answer using only the documents above. If the documents don't contain enough information, say "I don't have enough information on that." """

    # Step 4: Call Groq
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        temperature=0.2  # low temp = more grounded, less creative
    )

    answer = response.choices[0].message.content.strip()

    # Step 5: Programmatically collect sources (not left to LLM)
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }