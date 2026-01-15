from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import time
import config  # Import centralized configuration

def create_database_and_collection():
    print(f"Connecting to MongoDB Atlas...")
    client = MongoClient(config.MONGO_URI)
    db = client[config.DATABASE_NAME]

    existing_collections = db.list_collection_names()

    if config.COLLECTION_NAME in existing_collections:
        print(f"Collection '{config.COLLECTION_NAME}' already exists.")
    else:
        print(f"Collection '{config.COLLECTION_NAME}' does not exist.")
        print("Creating collection by inserting a temporary document...")
        collection = db[config.COLLECTION_NAME]
        result = collection.insert_one({"_id": "init_temp_doc", "info": "Temporary doc"})
        print(f"Collection created! Inserted temp doc ID: {result.inserted_id}")
        collection.delete_one({"_id": "init_temp_doc"})
        print("Temporary document deleted.")

    return db

def create_vector_search_index(db):
    collection = db[config.COLLECTION_NAME]
    print(f"\nCreating Vector Search Index '{config.VECTOR_INDEX_NAME}'...")

    # Correct Vector Search definition
    index_definition = {
        "fields": [
            {
                "type": "vector",
                "path": config.EMBEDDING_PATH,
                "numDimensions": config.EMBEDDING_DIMENSIONS,
                "similarity": config.SIMILARITY_METRIC
            }
        ]
    }

    try:
        # Use SearchIndexModel for correct type specification
        search_index_model = SearchIndexModel(
            definition=index_definition,
            name=config.VECTOR_INDEX_NAME,
            type="vectorSearch"  
        )

        result = collection.create_search_indexes([search_index_model])

        print(f"✓ Vector Search Index '{config.VECTOR_INDEX_NAME}' creation initiated!")
        print(f"  Result: {result}")
        print(f"\nIMPORTANT: Index building happens in the background.")
        print(f"Please wait 1-2 minutes before running search queries.")

    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"Index '{config.VECTOR_INDEX_NAME}' already exists.")
        else:
            print(f"Error creating index: {e}")
            print(f"\nIf this fails, please use Atlas UI:")
            print(f"1. Go to Database > Search Indexes")
            print(f"2. Create Search Index > JSON Editor")
            print(f"3. Index Name: {config.VECTOR_INDEX_NAME}")
            print(f"4. Paste this JSON:")
            print(f"""
{{
  "fields": [
    {{
      "type": "vector",
      "path": "{config.EMBEDDING_PATH}",
      "numDimensions": {config.EMBEDDING_DIMENSIONS},
      "similarity": "{config.SIMILARITY_METRIC}"
    }}
  ]
}}
""")

def main():
    print("="*60)
    print("MongoDB Atlas Setup Script (Using config.py)")
    print("="*60)

    db = create_database_and_collection()

    print(f"\nProceed to create Vector Search Index?")
    proceed = input("Enter 'yes' to continue: ")

    if proceed.lower() == 'yes':
        create_vector_search_index(db)
    else:
        print("Skipped index creation.")

if __name__ == "__main__":
    main()
