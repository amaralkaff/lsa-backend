import pytest
from httpx import AsyncClient
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_partner(async_client: AsyncClient):
    """Test menambahkan partner baru"""
    # Login terlebih dahulu untuk mendapatkan token
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    await async_client.post("/auth/register", json=user_data)
    
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = await async_client.post("/auth/login", json=login_data)
    token = response.json()["data"]["access_token"]
    
    # Tambah partner baru
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buat file logo dummy
    logo_content = b"dummy logo content"
    logo = BytesIO(logo_content)
    
    files = {
        "logo": ("test.jpg", logo, "image/jpeg"),
        "name": (None, "Test Partner"),
        "description": (None, "This is a test partner description"),
        "website_url": (None, "https://www.example.com/")
    }
    
    try:
        response = await async_client.post("/partners", files=files, headers=headers)
        logger.info(f"Create partner response: {response.status_code} - {response.text}")
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Partner berhasil ditambahkan"
        assert data["data"]["name"] == "Test Partner"
        assert data["data"]["description"] == "This is a test partner description"
        assert data["data"]["website_url"] == "https://www.example.com/"
        assert "logo" in data["data"]
        return data["data"]
    except Exception as e:
        logger.error(f"Error in test_create_partner: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_partners(async_client: AsyncClient):
    """Test mengambil daftar partner"""
    # Tambah partner terlebih dahulu
    partner = await test_create_partner(async_client)
    
    try:
        response = await async_client.get("/partners")
        logger.info(f"Get partners response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Daftar partner berhasil diambil"
        assert len(data["data"]) > 0
        assert data["data"][0]["name"] == partner["name"]
    except Exception as e:
        logger.error(f"Error in test_get_partners: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_partner_by_id(async_client: AsyncClient):
    """Test mengambil detail partner"""
    # Tambah partner terlebih dahulu
    partner = await test_create_partner(async_client)
    
    try:
        response = await async_client.get(f"/partners/{partner['_id']}")
        logger.info(f"Get partner response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Detail partner berhasil diambil"
        assert data["data"]["name"] == partner["name"]
        assert data["data"]["description"] == partner["description"]
        assert data["data"]["website_url"] == partner["website_url"]
    except Exception as e:
        logger.error(f"Error in test_get_partner_by_id: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_partner_not_found(async_client: AsyncClient):
    """Test mengambil partner yang tidak ada"""
    try:
        response = await async_client.get("/partners/000000000000000000000000")
        logger.info(f"Get non-existent partner response: {response.status_code} - {response.text}")
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
        assert data["message"] == "Partner tidak ditemukan"
    except Exception as e:
        logger.error(f"Error in test_get_partner_not_found: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_delete_partner(async_client: AsyncClient):
    """Test menghapus partner"""
    # Tambah partner terlebih dahulu
    partner = await test_create_partner(async_client)
    
    # Login untuk mendapatkan token
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = await async_client.post("/auth/login", json=login_data)
    token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = await async_client.delete(f"/partners/{partner['_id']}", headers=headers)
        logger.info(f"Delete partner response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Partner berhasil dihapus"
        
        # Verifikasi partner sudah terhapus
        response = await async_client.get(f"/partners/{partner['_id']}")
        assert response.status_code == 404
    except Exception as e:
        logger.error(f"Error in test_delete_partner: {str(e)}")
        raise 