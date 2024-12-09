import pymongo
import subprocess

# MongoDB connection details
MONGO_URI = "mongodb+srv://saraswatabhi0007:abhishek@cluster1.cfcdeiv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
DB_NAME = "vpn_db"
COLLECTION_NAME = "users-vpn"
WG_CONFIG_PATH = "/etc/wireguard/wg0.conf"

def create_table(username):
    """
    Generate keys for a new user, store in MongoDB, and update wg0.conf.
    """
    try:
        # Generate keys
        private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
        public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode().strip()
        
        # Add to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_one({"username": username, "vpn_access": True, "public_key": public_key})
        print(f"User '{username}' added to MongoDB with public key.")

        # Add to wg0.conf
        with open(WG_CONFIG_PATH, "a") as conf_file:
            conf_file.write(f"\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = 10.0.0.{collection.count_documents({}) + 1}/32\n")
        print(f"WireGuard configuration updated for '{username}'.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    username_to_add = "test_user4"
    create_table(username_to_add)    