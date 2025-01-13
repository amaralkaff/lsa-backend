from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging
import asyncio
from typing import Optional
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

# MongoDB Client
client: Optional[AsyncIOMotorClient] = None
db = None

# Retry settings
MAX_RETRIES = 5
RETRY_DELAY = 2

async def connect_to_mongo():
    """Create database connection with retry mechanism."""
    global client, db
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            # Setup koneksi MongoDB
            client = AsyncIOMotorClient(settings.MONGODB_URL)
            
            # Test koneksi
            await client.admin.command('ping')
            server_info = await client.server_info()
            logger.info(f"Connected to MongoDB version: {server_info.get('version')}")
            
            db = client[settings.MONGODB_DATABASE]
            logger.info(f"Successfully connected to database: {settings.MONGODB_DATABASE}")
            return
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            retries += 1
            if retries == MAX_RETRIES:
                logger.error(f"Failed to connect to MongoDB after {MAX_RETRIES} attempts: {str(e)}")
                raise e
            
            logger.warning(f"Connection attempt {retries} failed. Retrying in {RETRY_DELAY} seconds... Error: {str(e)}")
            await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"Unexpected error while connecting to MongoDB: {str(e)}")
            raise e

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
        await client.admin.command('ping')
    except Exception as e:
        logger.warning(f"Lost connection to MongoDB: {str(e)}. Attempting to reconnect...")
        await connect_to_mongo()
    
    # Use test database if in testing mode
    if settings.MONGODB_DATABASE == settings.MONGODB_TEST_DB:
        return client[settings.MONGODB_TEST_DB]
    
    return db

async def get_collection(collection_name: str):
    """Get a specific collection with automatic database connection."""
    database = await get_database()
    return database[collection_name]
