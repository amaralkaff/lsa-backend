import pytest
from httpx import AsyncClient
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_gallery(async_client: AsyncClient):
    """Test menambahkan foto ke galeri"""
    # Login terlebih dahulu untuk mendapatkan token
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    await async_client.post("/auth/register", json=user_data)
    
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = await async_client.post("/auth/login", json=login_data)
    token = response.json()["data"]["access_token"]
    
    # Tambah foto ke galeri
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buat file gambar dummy
    image_content = b"dummy image content"
    image = BytesIO(image_content)
    
    files = {
        "image": ("test.jpg", image, "image/jpeg"),
        "title": (None, "Test Gallery Photo"),
        "description": (None, "This is a test gallery photo")
    }
    
    try:
        response = await async_client.post("/gallery", files=files, headers=headers)
        logger.info(f"Create gallery response: {response.status_code} - {response.text}")
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Foto berhasil ditambahkan"
        assert data["data"]["title"] == "Test Gallery Photo"
        assert data["data"]["description"] == "This is a test gallery photo"
        assert "image" in data["data"]
        return data["data"]
    except Exception as e:
        logger.error(f"Error in test_create_gallery: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_galleries(async_client: AsyncClient):
    """Test mengambil daftar foto galeri"""
    # Tambah foto terlebih dahulu
    gallery = await test_create_gallery(async_client)
    
    try:
        response = await async_client.get("/gallery")
        logger.info(f"Get galleries response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Daftar foto berhasil diambil"
        assert len(data["data"]) > 0
        assert data["data"][0]["title"] == gallery["title"]
    except Exception as e:
        logger.error(f"Error in test_get_galleries: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_gallery_by_id(async_client: AsyncClient):
    """Test mengambil detail foto"""
    # Tambah foto terlebih dahulu
    gallery = await test_create_gallery(async_client)
    
    try:
        response = await async_client.get(f"/gallery/{gallery['_id']}")
        logger.info(f"Get gallery response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Detail foto berhasil diambil"
        assert data["data"]["title"] == gallery["title"]
        assert data["data"]["description"] == gallery["description"]
    except Exception as e:
        logger.error(f"Error in test_get_gallery_by_id: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_gallery_not_found(async_client: AsyncClient):
    """Test mengambil foto yang tidak ada"""
    try:
        response = await async_client.get("/gallery/000000000000000000000000")
        logger.info(f"Get non-existent gallery response: {response.status_code} - {response.text}")
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
        assert data["message"] == "Foto tidak ditemukan"
    except Exception as e:
        logger.error(f"Error in test_get_gallery_not_found: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_delete_gallery(async_client: AsyncClient):
    """Test menghapus foto"""
    # Tambah foto terlebih dahulu
    gallery = await test_create_gallery(async_client)
    
    # Login untuk mendapatkan token
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = await async_client.post("/auth/login", json=login_data)
    token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = await async_client.delete(f"/gallery/{gallery['_id']}", headers=headers)
        logger.info(f"Delete gallery response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Foto berhasil dihapus"
        
        # Verifikasi foto sudah terhapus
        response = await async_client.get(f"/gallery/{gallery['_id']}")
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
        assert data["message"] == "Foto tidak ditemukan"
    except Exception as e:
        logger.error(f"Error in test_delete_gallery: {str(e)}")
        raise 