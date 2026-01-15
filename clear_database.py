from pymongo import MongoClient
import config  # Import centralized configuration

def clear_collection():
    print(f"Connecting to MongoDB...")
    client = MongoClient(config.MONGO_URI)
    db = client[config.DATABASE_NAME]
    collection = db[config.COLLECTION_NAME]

    # Check count before deletion
    count_before = collection.count_documents({})

    if count_before == 0:
        print(f"Collection '{config.COLLECTION_NAME}' is already empty.")
        return

    print(f"Found {count_before} documents.")
    confirm = input(f"WARNING: Are you sure you want to delete ALL {count_before} documents? (yes/no): ")

    if confirm.lower() == 'yes':
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents.")

        # Verify count is zero
        count_after = collection.count_documents({})
        print(f"Total documents remaining: {count_after}")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    clear_collection()
