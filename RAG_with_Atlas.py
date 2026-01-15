import requests
import json
from pymongo import MongoClient
import config  # Import centralized configuration

# --- HELPER FUNCTION: Get Embedding ---
def get_embedding(text):
    """Using Ollama to generate embedding"""
    payload = {
        "model": config.EMBEDDING_MODEL,
        "prompt": text
    }
    response = requests.post(config.EMBEDDINGS_URL, json=payload)
    return response.json()["embedding"]

# --- 1. USER QUERY ---
query_text = "What is RAG and why is it useful?"
print(f"\033[96mQuery: {query_text}\033[0m")

# --- 2. VECTOR SEARCH (RETRIEVAL) ---
q_emb = get_embedding(query_text)

# Connect to MongoDB
client = MongoClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]
collection = db[config.COLLECTION_NAME]

# Perform vector search using aggregation pipeline
pipeline = [
    {
        "$vectorSearch": {
            "index": config.VECTOR_INDEX_NAME,
            "path": config.EMBEDDING_PATH,
            "queryVector": q_emb,
            "numCandidates": 50,
            "limit": 3
        }
    },
    {
        "$project": {
            "content": 1
        }
    }
]

res = list(collection.aggregate(pipeline))

if not res:
    print(f"\033[91mError: No documents found! Check index '{config.VECTOR_INDEX_NAME}' or data.\033[0m")
    client.close()
    exit()

# --- 3. LLM GENERATION ---
context = "\n".join([doc["content"] for doc in res])
print(f"\033[90mFound {len(res)} relevant docs.\033[0m")

prompt = f"""Use ONLY the context below to answer the question.
Context:
{context}

Question: {query_text}
"""

payload = {
    "model": config.LLM_MODEL,
    "prompt": prompt,
    "stream": False
}

print("\033[93mGenerating answer...\033[0m")
response = requests.post(config.GENERATE_URL, json=payload, headers={"Content-Type": "application/json"})
response_data = response.json()

# --- 4. OUTPUT ---
print("\033[92m\nFinal Answer:\033[0m")
print(response_data["response"])

# Close MongoDB connection
client.close()
