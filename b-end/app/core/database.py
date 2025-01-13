from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

# MongoDB Client
client: Optional[AsyncIOMotorClient] = None # type: ignore
db = None

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

async def connect_to_mongo():
    """Create database connection with retry mechanism."""
    global client, db
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            # Setup connection pool
            client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                maxPoolSize=10,
                minPoolSize=1,
                maxIdleTimeMS=30000,
                connectTimeoutMS=5000,
                retryWrites=True
            )
            db = client[settings.MONGODB_DATABASE]
            
            # Test the connection
            await client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
            return
            
        except Exception as e:
            retries += 1
            if retries == MAX_RETRIES:
                logger.error(f"Failed to connect to MongoDB after {MAX_RETRIES} attempts: {e}")
                raise e
            
            logger.warning(f"Connection attempt {retries} failed. Retrying in {RETRY_DELAY} seconds...")
            await asyncio.sleep(RETRY_DELAY)

async def close_mongo_connection():
    """Close database connection."""
    global client
    if client is not None:
        client.close()
        logger.info("MongoDB connection closed.")

async def get_database():
    """Get database instance with automatic reconnection."""
    global client, db
    
    if client is None:
        await connect_to_mongo()
    
    try:
        # Test if connection is still alive
        await client.admin.command('ping')  # type: ignore
    except Exception as e:
        logger.warning(f"Lost connection to MongoDB: {e}. Attempting to reconnect...")
        await connect_to_mongo()
    
    # Use test database if in testing mode
    if settings.MONGODB_DATABASE == settings.MONGODB_TEST_DB:
        return client[settings.MONGODB_TEST_DB]  # type: ignore
    
    return db

async def get_collection(collection_name: str):
    """Get a specific collection with automatic database connection."""
    database = await get_database()
    return database[collection_name]
