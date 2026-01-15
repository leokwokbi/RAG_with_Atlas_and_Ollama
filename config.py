import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# --- MONGODB CONFIGURATION ---
# Use an environment variable for the connection string
# Default to a placeholder or local connection for safety if not set
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<username>:<password>@cluster.example.mongodb.net/?appName=MongoDB")
DATABASE_NAME = "mydb"
COLLECTION_NAME = "mycollection"
VECTOR_INDEX_NAME = "vector_index"

# --- OLLAMA CONFIGURATION ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11435")
GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
EMBEDDINGS_URL = f"{OLLAMA_BASE_URL}/api/embeddings"

# Models
LLM_MODEL = "llama3"
EMBEDDING_MODEL = "nomic-embed-text"

# --- VECTOR SEARCH CONFIGURATION ---
EMBEDDING_DIMENSIONS = 768
EMBEDDING_PATH = "embedding"
SIMILARITY_METRIC = "cosine"
