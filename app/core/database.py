from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGODB_URL = config("MONGODB_URL", default="mongodb://localhost:27017")
DATABASE_NAME = config("DATABASE_NAME", default="lembaga_sinergi_analitika")

# MongoDB Client
client = None
db = None

async def connect_to_mongo():
    """Create database connection."""
    global client, db
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        # Test the connection
        await client.admin.command('ping')
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection."""
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed.")

async def get_database():
    """Get database instance."""
    global client, db
    if db is None:
        await connect_to_mongo()
    return db
