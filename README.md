# RAG with MongoDB Atlas & Ollama

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline using **MongoDB Atlas Vector Search** for storage and retrieval, and **Ollama** (running locally) for embedding generation and LLM inference.

It allows you to store a knowledge base as vector embeddings in MongoDB and query it using natural language, ensuring the LLM's responses are grounded in your specific data.

## 🚀 Features

- **Automated Setup**: Scripts to automatically create Database, Collections, and Vector Search Indexes in Atlas.
- **Local AI**: Uses local Ollama instance for privacy and cost-efficiency (supports `llama3`, `nomic-embed-text`, etc.).
- **Vector Search**: Leverages MongoDB Atlas's native vector search capabilities.
- **Resource Management**: Utilities to easily clear data or delete entire databases/indexes.
- **Secure Config**: Uses `.env` for managing sensitive connection strings.

## 📋 Prerequisites

1.  **MongoDB Atlas Cluster**: You need a MongoDB Atlas account and a cluster (Free Tier works).
2.  **Ollama**: Installed and running locally.
    *   Download from [ollama.com](https://ollama.com).
    *   Pull the required models:
        ```bash
        ollama pull llama3
        ollama pull nomic-embed-text
        ```
3.  **Python 3.8+**

## 🛠️ Installation

1.  **Clone the repository** (if applicable) or download the scripts.

2.  **Install Python dependencies**:
    ```bash
    pip install pymongo requests python-dotenv
    ```

3.  **Configure Environment**:
    *   Rename `.env.example` to `.env`.
    *   Edit `.env` and add your MongoDB Atlas Connection String:
        ```env
        MONGO_URI="mongodb+srv://<user>:<password>@cluster.mongodb.net/?appName=MongoDB"
        ```

## 🏃 Usage Guide

Follow these steps to get the RAG system running:

### 1. Setup Database & Index
Initialize the database, collection, and create the required Vector Search Index.
```bash
python setup_database.py
```
*Note: Index creation on Atlas may take 1-2 minutes.*

### 2. Embed & Insert Knowledge
Convert your text data into vectors and store them in MongoDB.
```bash
python embed_knowledge.py
```
*You can modify the `knowledge_base` list inside this script to add your own data.*

### 3. Run RAG Query
Ask questions against your knowledge base.
```bash
python RAG_with_Atlas.py
```
This script will:
1.  Convert your question to a vector.
2.  Search MongoDB for relevant documents.
3.  Send the context + question to Ollama (Llama 3).
4.  Print the grounded answer.

## 🔧 Management Utilities

*   **Check/Clear Data**:
    View current document count or delete all documents in the collection.
    ```bash
    python clear_database.py
    ```

*   **Delete Resources**:
    Menu-driven tool to delete the Database, Collection, or Search Index.
    ```bash
    python delete_resources.py
    ```

## 📂 Project Structure

*   `config.py`: Central configuration loading variables from `.env`.
*   `setup_database.py`: Creates DB, Collection, and Vector Index.
*   `embed_knowledge.py`: Generates embeddings and inserts data.
*   `RAG_with_Atlas.py`: Performs the RAG search and generation.
*   `delete_resources.py`: Advanced resource cleanup tool.
*   `clear_database.py`: Simple utility to empty the collection.
*   `.env`: Stores sensitive MongoDB credentials (not committed to git).

## ⚠️ Troubleshooting

*   **Connection Errors**: Ensure your IP is whitelisted in MongoDB Atlas Network Access.
*   **Dimension Mismatch**: Ensure your Vector Index dimensions (default 768) match the embedding model (e.g., `nomic-embed-text`). If you use `llama3` for embeddings, you must change dimensions to 4096 in `config.py`.
*   **Index Not Found**: If queries fail immediately after setup, wait a minute for the Atlas Index to finish building.
