import pymongo
import sys

# MongoDB connection details
MONGO_URI = "mongodb+srv://saraswatabhi0007:abhishek@cluster0.g2qz7.mongodb.net/mdm"
DB_NAME = "vpn_db"
COLLECTION_NAME = "users-vpn"

def create_user(username):
    """
    Add a user with VPN access to the database.
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        print("Connected to MongoDB successfully!")

        # Access the database and collection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Insert the user
        user_data = {"username": username, "vpn_access": True}
        result = collection.insert_one(user_data)
        
        print(f"User '{username}' added with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error occurred while creating user: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Specify the username
    username_to_add = "test_user3"
    create_user(username_to_add)
