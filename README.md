# RAG with MongoDB Atlas & Ollama

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline using **MongoDB Atlas Vector Search** for storage and retrieval, and **Ollama** (running locally) for embedding generation and LLM inference.

It allows you to store a knowledge base as vector embeddings in MongoDB and query it using natural language, ensuring the LLM's responses are grounded in your specific data.

## 🚀 Features

- **Automated Setup**: Scripts to automatically create Database, Collections, and Vector Search Indexes in Atlas.
- **Local AI**: Uses local Ollama instance for privacy and cost-efficiency (supports `llama3`, `nomic-embed-text`, etc.).
- **Vector Search**: Leverages MongoDB Atlas's native vector search capabilities.
- **Resource Management**: Utilities to easily clear data or delete entire databases/indexes.
- **Cluster Management**: Pause, resume, or terminate Atlas clusters via API.
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
    *   (Optional) For cluster management, add Atlas API credentials:
        ```env
        ATLAS_PUBLIC_KEY="your_public_key"
        ATLAS_PRIVATE_KEY="your_private_key"
        ATLAS_PROJECT_ID="your_project_id"
        ATLAS_CLUSTER_NAME="Cluster0"
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

### Data Management

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

### Cluster Management

*   **Manage Cluster** (Pause/Resume/Terminate):
    Control your Atlas cluster state to save costs.
    ```bash
    python manage_cluster.py
    ```

    **Menu Options:**
    1. Check Status - View current cluster state
    2. Pause Cluster - Pause to save costs (M10+ only)
    3. Resume Cluster - Resume a paused cluster
    4. Terminate Cluster - Permanently delete cluster
    5. Exit

    **Requirements:**
    - Atlas API Key with Project Owner or Cluster Manager permissions
    - Update `.env` with `ATLAS_PUBLIC_KEY`, `ATLAS_PRIVATE_KEY`, `ATLAS_PROJECT_ID`, and `ATLAS_CLUSTER_NAME`

    **Note:** Free Tier (M0) clusters cannot be paused, only M10+ paid clusters support pausing.

## 📂 Project Structure

*   `config.py`: Central configuration loading variables from `.env`.
*   `setup_database.py`: Creates DB, Collection, and Vector Index.
*   `embed_knowledge.py`: Generates embeddings and inserts data.
*   `RAG_with_Atlas.py`: Performs the RAG search and generation.
*   `delete_resources.py`: Advanced resource cleanup tool.
*   `clear_database.py`: Simple utility to empty the collection.
*   `manage_cluster.py`: Atlas cluster management (pause/resume/terminate).
*   `.env`: Stores sensitive MongoDB credentials (not committed to git).

## 🔑 Getting Atlas API Credentials

To use `manage_cluster.py`, you need to generate API keys:

1. Log in to MongoDB Atlas
2. Go to **Access Manager** > **Project Access**
3. Click **Create API Key**
4. Set **Description** (e.g., "Python Cluster Manager")
5. Select **Project Permissions**: **Project Owner** or **Cluster Manager**
6. Copy the **Public Key** and **Private Key**
7. **Important**: Add your IP address to the API Access List (Whitelist)
8. Get your **Project ID** from **Project Settings**

Add these credentials to your `.env` file.

## ⚠️ Troubleshooting

*   **Connection Errors**: Ensure your IP is whitelisted in MongoDB Atlas Network Access.
*   **Dimension Mismatch**: Ensure your Vector Index dimensions (default 768) match the embedding model (e.g., `nomic-embed-text`). If you use `llama3` for embeddings, you must change dimensions to 4096 in `config.py`.
*   **Index Not Found**: If queries fail immediately after setup, wait a minute for the Atlas Index to finish building.
*   **API Authentication Errors**: Verify your API keys are correct and your IP is whitelisted in the API Access List.
*   **Cannot Pause M0 Cluster**: Free tier (M0) clusters do not support pausing; only M10+ paid clusters can be paused.

## 📝 License

This project is open source and available under the MIT License.
