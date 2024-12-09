import pymongo

MONGO_URI = "mongodb+srv://saraswatabhi0007:abhishek@cluster0.g2qz7.mongodb.net/mdm"
DB_NAME = "vpn_db"
COLLECTION_NAME = "users-vpn"
WG_CONFIG_PATH = "/etc/wireguard/wg0.conf"

def update_wireguard_config():
    """
    Fetch users from MongoDB and update WireGuard configuration file.
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        print("Connected to MongoDB successfully!")

        # Access the database and collection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Fetch allowed users
        users = collection.find({"vpn_access": True})

        # Generate WireGuard configuration
        config = [
            "[Interface]",
            "PrivateKey = YOUR_SERVER_PRIVATE_KEY",
            "Address = 10.0.0.1/24",
            "ListenPort = 51820",
            ""
        ]

        for user in users:
            public_key = user.get("public_key")
            if public_key:
                config += [
                    "[Peer]",
                    f"PublicKey = {public_key}",
                    "AllowedIPs = 10.0.0.2/32",
                    ""
                ]

        # Write the configuration to file
        with open(WG_CONFIG_PATH, "w") as config_file:
            config_file.write("\n".join(config))

        print(f"WireGuard configuration updated at {WG_CONFIG_PATH}!")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    update_wireguard_config()
