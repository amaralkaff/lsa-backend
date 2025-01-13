import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.core.config import settings
import asyncio
import os
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def set_test_db():
    """Set test database."""
    settings.MONGODB_DATABASE = settings.MONGODB_TEST_DB
    return settings

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_client(event_loop):
    """Create database client."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_TEST_DB]
    
    # Bersihkan koleksi sebelum test
    try:
        collections = await db.list_collection_names()
        for collection in collections:
            await db[collection].delete_many({})
            logger.info(f"Cleaned collection: {collection}")
    except Exception as e:
        logger.error(f"Error cleaning collections before test: {e}")
    
    # Set database test ke aplikasi
    app.state.db = db
    
    yield db
    
    # Bersihkan koleksi setelah test
    try:
        collections = await db.list_collection_names()
        for collection in collections:
            await db[collection].delete_many({})
            logger.info(f"Cleaned collection after test: {collection}")
    except Exception as e:
        logger.error(f"Error cleaning collections after test: {e}")
    
    client.close()

@pytest_asyncio.fixture(scope="function")
async def async_client(db_client):
    """Create async client."""
    app.state.db = db_client
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client 