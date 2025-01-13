import pytest
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient, db_client):
    """Test registrasi berhasil"""
    # Periksa collection users sebelum test
    users = await db_client["users"].find({}).to_list(None) # type: ignore
    logger.info(f"Users before test: {users}")
    
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    try:
        response = await async_client.post("/auth/register", json=user_data)
        logger.info(f"Register response: {response.status_code} - {response.text}")
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "password" not in data
        assert data["is_active"] == True
    except Exception as e:
        logger.error(f"Error in test_register_success: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    """Test login berhasil"""
    # Register user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    await async_client.post("/auth/register", json=user_data)
    
    # Login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    try:
        response = await async_client.post("/auth/login", data=login_data)
        logger.info(f"Login response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    except Exception as e:
        logger.error(f"Error in test_login_success: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient):
    """Test registrasi dengan email yang sudah terdaftar"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser2",
        "password": "testpassword123"
    }
    # Register first user
    await async_client.post("/auth/register", json=user_data)
    
    # Try to register with same email
    try:
        response = await async_client.post("/auth/register", json=user_data)
        logger.info(f"Duplicate email response: {response.status_code} - {response.text}")
        assert response.status_code == 400
        assert "Email sudah terdaftar" in response.json()["detail"]
    except Exception as e:
        logger.error(f"Error in test_register_duplicate_email: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_register_duplicate_username(async_client: AsyncClient):
    """Test registrasi dengan username yang sudah digunakan"""
    # Register first user
    user1_data = {
        "email": "test1@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    await async_client.post("/auth/register", json=user1_data)
    
    # Try to register with same username
    user2_data = {
        "email": "test2@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    try:
        response = await async_client.post("/auth/register", json=user2_data)
        logger.info(f"Duplicate username response: {response.status_code} - {response.text}")
        assert response.status_code == 400
        assert "Username sudah digunakan" in response.json()["detail"]
    except Exception as e:
        logger.error(f"Error in test_register_duplicate_username: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient):
    """Test login dengan password yang salah"""
    # Register user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    await async_client.post("/auth/register", json=user_data)
    
    # Try to login with wrong password
    login_data = {
        "username": user_data["email"],
        "password": "wrongpassword"
    }
    try:
        response = await async_client.post("/auth/login", data=login_data)
        logger.info(f"Wrong password response: {response.status_code} - {response.text}")
        assert response.status_code == 400
        assert "Email atau password salah" in response.json()["detail"]
    except Exception as e:
        logger.error(f"Error in test_login_wrong_password: {str(e)}")
        raise 