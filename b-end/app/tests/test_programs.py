import pytest
from httpx import AsyncClient
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_program(async_client: AsyncClient):
    """Test membuat program baru"""
    # Login terlebih dahulu untuk mendapatkan token
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123456"  # Minimal 8 karakter
    }
    register_response = await async_client.post("/auth/register", json=user_data)
    print(f"Register response: {register_response.status_code} - {register_response.text}")
    assert register_response.status_code == 201
    
    # Login langsung dengan credentials
    login_response = await async_client.post("/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    print(f"Login response: {login_response.status_code} - {login_response.text}")
    assert login_response.status_code == 200
    login_data = login_response.json()
    token = login_data["data"]["access_token"]
    
    # Buat program baru dengan gambar dummy minimal
    headers = {"Authorization": f"Bearer {token}"}
    image = BytesIO(b"x")
    
    # Gunakan waktu statis untuk menghindari kalkulasi
    files = {
        "image": ("t.jpg", image, "image/jpeg"),
        "title": (None, "Test"),
        "description": (None, "Test desc"),
        "program_type": (None, "workshop"),
        "start_date": (None, "2024-01-01T00:00:00"),
        "end_date": (None, "2024-01-02T00:00:00")
    }
    
    response = await async_client.post("/programs", files=files, headers=headers)
    print(f"Create program response: {response.status_code} - {response.text}")
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Program berhasil dibuat"
    assert data["data"]["title"] == "Test"
    return data["data"]

@pytest.mark.asyncio
async def test_get_programs(async_client: AsyncClient):
    """Test mengambil daftar program"""
    program = await test_create_program(async_client)
    
    response = await async_client.get("/programs")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Daftar program berhasil diambil"
    assert len(data["data"]) > 0
    assert data["data"][0]["title"] == program["title"]

@pytest.mark.asyncio
async def test_get_programs_by_type(async_client: AsyncClient):
    """Test mengambil daftar program berdasarkan tipe"""
    await test_create_program(async_client)
    
    response = await async_client.get("/programs?program_type=workshop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Daftar program berhasil diambil"
    assert len(data["data"]) > 0
    assert data["data"][0]["program_type"] == "workshop"

@pytest.mark.asyncio
async def test_get_program_by_id(async_client: AsyncClient):
    """Test mengambil detail program"""
    program = await test_create_program(async_client)
    
    response = await async_client.get(f"/programs/{program['_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Detail program berhasil diambil"
    assert data["data"]["title"] == program["title"]

@pytest.mark.asyncio
async def test_get_program_not_found(async_client: AsyncClient):
    """Test mengambil program yang tidak ada"""
    response = await async_client.get("/programs/000000000000000000000000")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Program tidak ditemukan"

@pytest.mark.asyncio
async def test_delete_program(async_client: AsyncClient):
    """Test menghapus program"""
    program = await test_create_program(async_client)
    
    # Login untuk mendapatkan token
    response = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123456"
    })
    token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await async_client.delete(f"/programs/{program['_id']}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Program berhasil dihapus"
    
    # Verifikasi program sudah terhapus
    response = await async_client.get(f"/programs/{program['_id']}")
    assert response.status_code == 404 