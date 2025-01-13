from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# MongoDB Client
client = None
db = None

async def connect_to_mongo():
    """Create database connection."""
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DATABASE]
        # Test the connection
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB.")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection."""
    global client
    if client is not None:
        client.close()
        logger.info("MongoDB connection closed.")

async def get_database():
    """Get database instance."""
    global client, db
    if db is None:
        await connect_to_mongo()
    # Jika sedang testing, gunakan database test
    if settings.MONGODB_DATABASE == settings.MONGODB_TEST_DB:
        return client[settings.MONGODB_TEST_DB]
    return db
