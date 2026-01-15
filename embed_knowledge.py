import requests
from pymongo import MongoClient
import config  # Import centralized configuration

# --- DATA ---
knowledge_base = [
    "Retrieval-Augmented Generation (RAG) is a method that retrieves data from an external database to ground LLM responses in reality.",
    "RAG prevents LLM hallucinations by forcing the model to use retrieved facts instead of training memory.",
    "MongoDB Atlas Vector Search stores high-dimensional embeddings (vectors) to enable fast semantic retrieval for RAG.",
    "In a RAG pipeline, the system first searches for relevant documents, then sends them as context to the LLM."
]

# --- HELPER FUNCTION ---
def get_embedding(text):
    """Generates embedding vector using Ollama"""
    try:
        payload = {
            "model": config.EMBEDDING_MODEL,
            "prompt": text
        }
        response = requests.post(config.EMBEDDINGS_URL, json=payload)
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

# --- MAIN EXECUTION ---
def main():
    print(f"Connecting to MongoDB...")
    client = MongoClient(config.MONGO_URI)
    db = client[config.DATABASE_NAME]
    collection = db[config.COLLECTION_NAME]

    documents_to_insert = []

    print(f"Processing {len(knowledge_base)} documents...")

    for i, text in enumerate(knowledge_base):
        print(f"  Embedding doc {i+1}/{len(knowledge_base)}...")
        embedding = get_embedding(text)

        if embedding:
            doc = {
                "content": text,
                "embedding": embedding,
                "source": "knowledge_base_script" # Optional metadata
            }
            documents_to_insert.append(doc)

    if documents_to_insert:
        print(f"Inserting {len(documents_to_insert)} documents into MongoDB...")
        result = collection.insert_many(documents_to_insert)
        print(f"Success! Inserted {len(result.inserted_ids)} documents.")

        # Count Total Documents
        total_count = collection.count_documents({})
        print(f"Total documents in '{config.COLLECTION_NAME}' is now: {total_count}")

    else:
        print("No documents were prepared for insertion.")

if __name__ == "__main__":
    main()
