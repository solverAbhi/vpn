import pymongo
import sys

# MongoDB connection details
MONGO_URI = "mongodb+srv://saraswatabhi0007:abhishek@cluster0.g2qz7.mongodb.net/mdm"
DB_NAME = "vpn_db"
COLLECTION_NAME = "users-vpn"

def authenticate_user(username):
    """
    Authenticate a user against the MongoDB database and collection.
    Checks if the user exists and has VPN access enabled.

    :param username: The username to authenticate.
    :return: True if authentication is successful, False otherwise.
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        print("Connected to MongoDB successfully!")

        # Access the database and collection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Query the collection for the user
        user = collection.find_one({"username": username, "vpn_access": True})

        if user:
            print(f"User '{username}' authenticated successfully!")
            return True
        else:
            print(f"Authentication failed for user '{username}'.")
            return False

    except Exception as e:
        print(f"Error occurred during authentication: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    # Example username for testing
    test_username = "test_user4"

    # Authenticate the user
    success = authenticate_user(test_username)
    sys.exit(0 if success else 1)
