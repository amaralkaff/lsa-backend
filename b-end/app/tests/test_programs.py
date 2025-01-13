import pytest
from httpx import AsyncClient
import logging
from io import BytesIO
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_program(async_client: AsyncClient):
    """Test membuat program baru"""
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
    
    # Buat program baru
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buat file gambar dummy
    image_content = b"dummy image content"
    image = BytesIO(image_content)
    
    # Set tanggal mulai dan selesai
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=1)
    
    files = {
        "image": ("test.jpg", image, "image/jpeg"),
        "title": (None, "Test Program"),
        "description": (None, "This is a test program"),
        "program_type": (None, "workshop"),
        "start_date": (None, start_date.isoformat()),
        "end_date": (None, end_date.isoformat())
    }
    
    try:
        response = await async_client.post("/programs", files=files, headers=headers)
        logger.info(f"Create program response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Program"
        assert data["description"] == "This is a test program"
        assert data["program_type"] == "workshop"
        assert "image" in data
        return data
    except Exception as e:
        logger.error(f"Error in test_create_program: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_programs(async_client: AsyncClient):
    """Test mengambil daftar program"""
    # Buat program terlebih dahulu
    program = await test_create_program(async_client)
    
    try:
        response = await async_client.get("/programs")
        logger.info(f"Get programs response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["title"] == program["title"]
    except Exception as e:
        logger.error(f"Error in test_get_programs: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_programs_by_type(async_client: AsyncClient):
    """Test mengambil daftar program berdasarkan tipe"""
    # Buat program terlebih dahulu
    program = await test_create_program(async_client)
    
    try:
        response = await async_client.get("/programs?program_type=workshop")
        logger.info(f"Get programs by type response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["program_type"] == "workshop"
    except Exception as e:
        logger.error(f"Error in test_get_programs_by_type: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_program_by_id(async_client: AsyncClient):
    """Test mengambil detail program"""
    # Buat program terlebih dahulu
    program = await test_create_program(async_client)
    
    try:
        response = await async_client.get(f"/programs/{program['_id']}")
        logger.info(f"Get program response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == program["title"]
        assert data["description"] == program["description"]
        assert data["program_type"] == program["program_type"]
    except Exception as e:
        logger.error(f"Error in test_get_program_by_id: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_get_program_not_found(async_client: AsyncClient):
    """Test mengambil program yang tidak ada"""
    try:
        response = await async_client.get("/programs/000000000000000000000000")
        logger.info(f"Get non-existent program response: {response.status_code} - {response.text}")
        assert response.status_code == 404
        assert "Program tidak ditemukan" in response.json()["detail"]
    except Exception as e:
        logger.error(f"Error in test_get_program_not_found: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_delete_program(async_client: AsyncClient):
    """Test menghapus program"""
    # Buat program terlebih dahulu
    program = await test_create_program(async_client)
    
    # Login untuk mendapatkan token
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = await async_client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = await async_client.delete(f"/programs/{program['_id']}", headers=headers)
        logger.info(f"Delete program response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        assert "Program berhasil dihapus" in response.json()["message"]
        
        # Verifikasi program sudah terhapus
        response = await async_client.get(f"/programs/{program['_id']}")
        assert response.status_code == 404
    except Exception as e:
        logger.error(f"Error in test_delete_program: {str(e)}")
        raise 