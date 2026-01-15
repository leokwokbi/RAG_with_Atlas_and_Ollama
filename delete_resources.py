from pymongo import MongoClient
import config  # Import centralized configuration

def get_db_client():
    return MongoClient(config.MONGO_URI)

def delete_database():
    confirm = input(f"\nWARNING: Drop ENTIRE database '{config.DATABASE_NAME}'? (Type 'DELETE' to confirm): ")
    if confirm == 'DELETE':
        client = get_db_client()
        client.drop_database(config.DATABASE_NAME)
        print(f"✓ Database '{config.DATABASE_NAME}' dropped.")
        client.close()
    else:
        print("Cancelled.")

def delete_collection():
    confirm = input(f"\nWARNING: Drop collection '{config.COLLECTION_NAME}'? (Type 'DELETE' to confirm): ")
    if confirm == 'DELETE':
        client = get_db_client()
        db = client[config.DATABASE_NAME]
        if config.COLLECTION_NAME in db.list_collection_names():
            db.drop_collection(config.COLLECTION_NAME)
            print(f"✓ Collection '{config.COLLECTION_NAME}' dropped.")
        else:
            print(f"Collection '{config.COLLECTION_NAME}' not found.")
        client.close()
    else:
        print("Cancelled.")

def delete_search_index():
    print(f"\nTarget Index: '{config.VECTOR_INDEX_NAME}' in collection '{config.COLLECTION_NAME}'")
    confirm = input(f"Confirm delete index? (Type 'DELETE' to confirm): ")
    if confirm == 'DELETE':
        client = get_db_client()
        db = client[config.DATABASE_NAME]
        collection = db[config.COLLECTION_NAME]
        try:
            # Note: PyMongo drop_index is for regular indexes. 
            # Search Indexes are managed differently.
            # We use the command helper or Atlas specific methods if available.
            # For Search Indexes, we usually use drop_search_index (available in newer pymongo)

            # Listing indexes first to check existence
            indexes = list(collection.list_search_indexes())
            index_exists = any(idx.get('name') == config.VECTOR_INDEX_NAME for idx in indexes)

            if index_exists:
                collection.drop_search_index(config.VECTOR_INDEX_NAME)
                print(f"✓ Search Index '{config.VECTOR_INDEX_NAME}' deletion initiated.")
            else:
                print(f"Search Index '{config.VECTOR_INDEX_NAME}' not found.")

        except Exception as e:
            print(f"Error deleting search index: {e}")
            print("Note: If using an older pymongo version, search index deletion might require Atlas UI.")

        client.close()
    else:
        print("Cancelled.")

def main():
    while True:
        print("\n" + "="*40)
        print("MongoDB Resource Manager")
        print("="*40)
        print(f"Target DB: {config.DATABASE_NAME}")
        print(f"Target Coll: {config.COLLECTION_NAME}")
        print(f"Target Search Index: {config.VECTOR_INDEX_NAME}")
        print("-" * 40)
        print("1. Delete Database (Drop everything)")
        print("2. Delete Collection only")
        print("3. Delete Search Index only")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ")

        if choice == '1':
            delete_database()
        elif choice == '2':
            delete_collection()
        elif choice == '3':
            delete_search_index()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
