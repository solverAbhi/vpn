import pymongo
import sys

# MongoDB connection details
MONGO_URI = "mongodb+srv://saraswatabhi0007:abhishek@cluster1.cfcdeiv.mongodb.net/"
DB_NAME = "vpn_db"
COLLECTION_NAME = "users-vpn"

def create_table():
    """
    Connect to MongoDB, create a database, and a collection.
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        print("Connected to MongoDB successfully!")

        # Access or create the database
        db = client[DB_NAME]

        # Access or create the collection
        collection = db[COLLECTION_NAME]

        # Insert a sample document (for testing purposes)
        sample_data = {"username": "test_user", "vpn_access": True}
        result = collection.insert_one(sample_data)
        
        print(f"Table '{COLLECTION_NAME}' created in database '{DB_NAME}'!")
        print(f"Sample document inserted with ID: {result.inserted_id}")

    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    create_table()
