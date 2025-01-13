import pytest
from httpx import AsyncClient
import logging
import os
from io import BytesIO

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_blog(async_client: AsyncClient):
    """Test membuat blog baru"""
    # Login terlebih dahulu untuk mendapatkan token
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    await async_client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = await async_client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Buat blog baru
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buat file gambar dummy
    image_content = b"dummy image content"
    image = BytesIO(image_content)
    
    files = {
        "image": ("test.jpg", image, "image/jpeg"),
        "title": (None, "Test Blog"),
        "content": (None, "This is a test blog content")
    }
    
    try:
        response = await async_client.post("/blogs", files=files, headers=headers)
        logger.info(f"Create blog response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Blog"
        assert data["content"] == "This is a test blog content"
        assert "image" in data
        return data
    except Exception as e:
        logger.error(f"Error in test_create_blog: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_blogs(async_client: AsyncClient):
    """Test mengambil daftar blog"""
    # Buat blog terlebih dahulu
    blog = await test_create_blog(async_client)
    
    try:
        response = await async_client.get("/blogs")
        logger.info(f"Get blogs response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) > 0
        assert data["data"][0]["title"] == blog["title"]
    except Exception as e:
        logger.error(f"Error in test_get_blogs: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_blog_by_id(async_client: AsyncClient):
    """Test mengambil detail blog"""
    # Buat blog terlebih dahulu
    blog = await test_create_blog(async_client)
    
    try:
        response = await async_client.get(f"/blogs/{blog['_id']}")
        logger.info(f"Get blog response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == blog["title"]
        assert data["content"] == blog["content"]
    except Exception as e:
        logger.error(f"Error in test_get_blog_by_id: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_blog_not_found(async_client: AsyncClient):
    """Test mengambil blog yang tidak ada"""
    try:
        response = await async_client.get("/blogs/000000000000000000000000")
        logger.info(f"Get non-existent blog response: {response.status_code} - {response.text}")
        assert response.status_code == 404
        assert "Blog tidak ditemukan" in response.json()["detail"]
    except Exception as e:
        logger.error(f"Error in test_get_blog_not_found: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_delete_blog(async_client: AsyncClient):
    """Test menghapus blog"""
    # Buat blog terlebih dahulu
    blog = await test_create_blog(async_client)
    
    # Login untuk mendapatkan token
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = await async_client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = await async_client.delete(f"/blogs/{blog['_id']}", headers=headers)
        logger.info(f"Delete blog response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        assert "Blog berhasil dihapus" in response.json()["message"]
        
        # Verifikasi blog sudah terhapus
        response = await async_client.get(f"/blogs/{blog['_id']}")
        assert response.status_code == 404
    except Exception as e:
        logger.error(f"Error in test_delete_blog: {str(e)}")
        raise 