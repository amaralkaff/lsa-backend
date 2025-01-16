# Panduan Lengkap Implementasi Backend FastAPI dan MongoDB

## TAHAP 1: SETUP PROJECT & ENVIRONMENT

### Langkah 1: Setup Environment

1. Buat folder project baru

```bash
mkdir backend # Membuat folder backend (mkdir = make directory)
cd backend # Masuk ke folder backend (cd = change directory)
touch .env # Membuat file .env (touch = create file)
```

2. Buat virtual environment

```bash
python -m venv venv # Membuat virtual environment (python -m venv = python module virtual environment)
```

3. Aktifkan virtual environment

- Windows:

```bash
venv\Scripts\activate # Aktifkan virtual environment (venv\Scripts\activate = virtual environment script)
```

atau

```bash
.\venv\Scripts\activate # Aktifkan virtual environment (.\venv\Scripts\activate = virtual environment script)
```

atau 

- Linux/Mac/Windows(Git Bash):
```bash
source venv/bin/activate # Aktifkan virtual environment (source venv/bin/activate = virtual environment script)
```

### Langkah 2: Install Dependencies

1. Install package utama

```bash
pip install fastapi uvicorn motor pydantic python-jose[cryptography] passlib[bcrypt] python-multipart python-decouple
```

atau

2. Buat requirements.txt

```bash
pip freeze > requirements.txt # Membuat requirements.txt (pip freeze = pip module freeze)
```

3. Install dependencies dari requirements.txt

```bash
pip install -r requirements.txt # Install dependencies dari requirements.txt

```

```txt
fastapi==0.115.6
uvicorn==0.34.0
motor==3.6.0
pymongo==4.9.2
python-decouple==3.8
python-multipart==0.0.20
pydantic==2.10.5
pydantic-settings==2.7.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2
email-validator==2.1.0.post1
dnspython==2.7.0

# Testing dependencies
pytest>=8.2.0
pytest-asyncio>=0.25.1
httpx==0.26.0
```

### Langkah 3: Penjelasan package utama

1. fastapi==0.115.6

   - Framework web modern dan cepat untuk membangun API
   - Berbasis Python modern (async/await)
   - Fitur validasi otomatis dan dokumentasi OpenAPI

2. uvicorn==0.34.0

   - Server ASGI yang cepat untuk menjalankan aplikasi FastAPI
   - Mendukung hot reload untuk development
   - Penanganan WebSocket

3. motor==3.6.0 & pymongo==4.9.2

   - Motor: Driver MongoDB async untuk Python
   - PyMongo: Driver MongoDB sync (diperlukan oleh Motor)
   - Menangani koneksi dan operasi database

4. python-decouple==3.8

   - Memisahkan konfigurasi dari kode
   - Membaca variabel environment
   - Memudahkan manajemen konfigurasi

5. python-multipart==0.0.20

   - Menangani form data dan file upload
   - Dibutuhkan untuk menerima request multipart/form-data
   - Penting untuk fitur upload file

6. pydantic==2.10.5 & pydantic-settings==2.7.1

   - Validasi data dan serialisasi
   - Type hints yang powerful
   - Integrasi dengan FastAPI untuk model data
   - Settings management dengan validasi

7. python-jose[cryptography]==3.3.0

   - Implementasi JWT (JSON Web Tokens)
   - Menangani enkripsi dan dekripsi token
   - Fitur keamanan untuk autentikasi

8. passlib[bcrypt]==1.7.4 & bcrypt==4.1.2

   - Passlib: Library untuk password hashing
   - Bcrypt: Algoritma hashing yang aman
   - Mengamankan password user

9. email-validator==2.1.0.post1 & dnspython==2.7.0
   - Validasi format email
   - Verifikasi domain email
   - Memastikan input email yang valid

10. Testing Dependencies:
    - pytest>=8.2.0: Framework testing Python
    - pytest-asyncio>=0.25.1: Plugin pytest untuk async testing
    - httpx==0.26.0: HTTP client async untuk testing API

### Langkah 4: Setup Struktur Project

1. Buat struktur folder berikut:

## Struktur Proyek
```
backend/
├── app/                        # Folder inti yang berisi seluruh logika aplikasi
│   ├── api/                    # Folder yang berisi semua endpoint API dan dependensi
│   │   ├── endpoints/          # Folder yang berisi semua endpoint API
│   │   │   ├── auth.py         # Endpoint untuk autentikasi (login, register)
│   │   │   ├── blog.py         # Endpoint untuk manajemen blog/artikel
│   │   │   ├── gallery.py      # Endpoint untuk manajemen galeri foto
│   │   │   ├── partners.py     # Endpoint untuk manajemen mitra/partner
│   │   │   └── programs.py     # Endpoint untuk manajemen program/kegiatan
│   │   └── deps.py             # Berisi dependency injection
│   ├── core/                   # Berisi komponen inti aplikasi
│   │   ├── config.py           # Konfigurasi aplikasi
│   │   ├── database.py         # Konfigurasi koneksi database MongoDB
│   │   └── security.py         # Konfigurasi keamanan JWT
│   ├── models/                 # Berisi model data
│   │   └── schemas.py          # Model untuk validasi data
│   ├── tests/                  # Berisi unit tests
│   │   ├── conftest.py         # Konfigurasi dan fixtures untuk testing
│   │   ├── test_auth.py        # Test untuk autentikasi
│   │   ├── test_blog.py        # Test untuk blog
│   │   ├── test_gallery.py     # Test untuk galeri
│   │   ├── test_partners.py    # Test untuk partner
│   │   └── test_programs.py    # Test untuk program
│   ├── utils/                  # Berisi utility functions
│   │   ├── file_handler.py     # Fungsi untuk menangani file uploads
│   │   ├── seeder.py           # Fungsi untuk menghasilkan data dummy
│   │   └── reset_db.py         # Fungsi untuk mereset database
│   └── main.py                 # File utama untuk menjalankan aplikasi
├── static/                     # Folder untuk menyimpan file static
│   └── uploads/                # Folder untuk menyimpan file uploads
├── venv/                       # Virtual environment Python
├── .env                        # File untuk environment variables
├── .env.example                # Contoh konfigurasi environment variables
├── .gitignore                  # File untuk mengabaikan file/folder dalam git
├── pytest.ini                  # Konfigurasi untuk pytest
├── requirements.txt            # Daftar package Python yang dibutuhkan
└── README.md                   # Dokumentasi proyek
```

### 1. Folder Root (`backend/`)

- Folder utama proyek
- Menyimpan file konfigurasi dan virtual environment

### 2. Folder `app/`

- Folder inti aplikasi
- Berisi modul-modul terpisah

### 3. Folder `app/api/`

- Folder endpoint API
- Berisi routing dan logika bisnis

#### 3.1 Folder `app/api/endpoints/`

- Folder berisi file-file endpoint untuk setiap fitur:
  - Autentikasi (login, register)
  - Blog (CRUD)
  - Galeri (CRUD)
  - Partner (CRUD)
  - Program (CRUD)

### 4. Folder `app/core/`

- Folder komponen inti
- Berisi konfigurasi dan koneksi database

### 5. Folder `app/models/`

- Folder model data
- Berisi skema validasi

### 6. Folder `app/tests/`

- Folder unit testing
- Berisi file test untuk setiap fitur

### 7. Folder `app/utils/`

- Folder fungsi utilitas
- Berisi file handler dan seeder

### 8. Folder `static/`

- Folder file statis
- Berisi file uploads

### Langkah 5: Jalankan project 

```bash
uvicorn main:app --reload # Menjalankan server FastAPI dengan hot reload
```

### Langkah 6: Setup Database Connection

1. Implementasi koneksi MongoDB di app/core/database.py:

```python
from motor.motor_asyncio import AsyncIOMotorClient # Library untuk koneksi MongoDB async
from app.core.config import settings # Pengaturan aplikasi
import logging # Untuk logging
import asyncio # Untuk async/await
from typing import Optional # Untuk tipe data opsional
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError # Error handling MongoDB

# Setup logging
logger = logging.getLogger(__name__)

# Variabel global untuk koneksi MongoDB
client: Optional[AsyncIOMotorClient] = None # Client MongoDB
db = None # Database

# Pengaturan retry
MAX_RETRIES = 5 # Jumlah maksimal percobaan koneksi
RETRY_DELAY = 2 # Jeda waktu antar percobaan dalam detik

async def connect_to_mongo():
    """Membuat koneksi ke database MongoDB dengan mekanisme retry."""
    global client, db
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            # Membuat koneksi ke MongoDB
            client = AsyncIOMotorClient(settings.MONGODB_URL)
            
            # Tes koneksi dengan ping
            await client.admin.command('ping')
            server_info = await client.server_info()
            logger.info(f"Terhubung ke MongoDB versi: {server_info.get('version')}")
            
            # Set database yang digunakan
            db = client[settings.MONGODB_DATABASE]
            logger.info(f"Berhasil terhubung ke database: {settings.MONGODB_DATABASE}")
            return
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            retries += 1
            if retries == MAX_RETRIES:
                logger.error(f"Gagal terhubung ke MongoDB setelah {MAX_RETRIES} percobaan: {str(e)}")
                raise e
            
            logger.warning(f"Percobaan koneksi ke-{retries} gagal. Mencoba lagi dalam {RETRY_DELAY} detik... Error: {str(e)}")
            await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"Error tidak terduga saat menghubungkan ke MongoDB: {str(e)}")
            raise e

async def close_mongo_connection():
    """Menutup koneksi database."""
    global client
    if client is not None:
        client.close()
        logger.info("Koneksi MongoDB ditutup.")

async def get_database():
    """Mendapatkan instance database dengan reconnect otomatis."""
    global client, db
    
    if client is None:
        await connect_to_mongo()
    
    try:
        # Tes apakah koneksi masih aktif
        await client.admin.command('ping')
    except Exception as e:
        logger.warning(f"Koneksi ke MongoDB terputus: {str(e)}. Mencoba menghubungkan kembali...")
        await connect_to_mongo()
    
    # Gunakan database test jika dalam mode testing
    if settings.MONGODB_DATABASE == settings.MONGODB_TEST_DB:
        return client[settings.MONGODB_TEST_DB]
    
    return db

async def get_collection(collection_name: str):
    """Mendapatkan koleksi spesifik dengan koneksi database otomatis."""
    database = await get_database()
    return database[collection_name]
```

Modul Database ini menyediakan fungsi-fungsi untuk:

1. Membuat koneksi ke MongoDB secara asynchronous
2. Menutup koneksi database dengan aman
3. Mendapatkan instance database untuk operasi CRUD

Fitur utama:

- Koneksi asynchronous menggunakan Motor
- Konfigurasi dari environment variables
- Auto-reconnect jika koneksi terputus
- Penanganan error koneksi
- Logging status koneksi
- Manajemen resource yang efisien

Keamanan:

- URL database dari environment variable
- Validasi koneksi dengan ping
- Penutupan koneksi yang aman
- Error handling untuk kegagalan koneksi

Penggunaan:

- Digunakan sebagai dependency di endpoint API
- Mendukung operasi database asynchronous
- Koneksi otomatis saat aplikasi startup
- Penutupan koneksi saat shutdown

### Langkah 2: Implementasi Schemas (schemas.py)

1. Buat base model dan utility class untuk ObjectId:

```python
# Import library yang diperlukan
from datetime import datetime  # Untuk menangani tanggal dan waktu
from typing import Optional, Any, Annotated, TypeVar, Generic  # Untuk type hints
from pydantic import BaseModel, Field, ConfigDict, HttpUrl, EmailStr, BeforeValidator  # Untuk validasi data
from bson import ObjectId  # Untuk menangani ObjectId MongoDB

# Fungsi validator untuk mengkonversi ObjectId ke string
def validate_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):  # Jika input berupa ObjectId
        return str(v)  # Konversi ke string
    if isinstance(v, str) and ObjectId.is_valid(v):  # Jika input string valid ObjectId
        return v  # Kembalikan string tersebut
    raise ValueError("Invalid ObjectId")  # Jika tidak valid, raise error

# Tipe kustom untuk ObjectId menggunakan Annotated
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]

# Generic type untuk ResponseEnvelope
T = TypeVar('T')  # Tipe variabel generik

# Model dasar untuk Program
class ProgramBase(BaseModel):
    title: str = Field(..., min_length=3, description="Judul program")  # Judul wajib diisi, min 3 karakter
    subtitle: str = Field(..., min_length=3, description="Sub judul program")  # Sub judul wajib diisi, min 3 karakter
    description: str = Field(..., description="Deskripsi lengkap program")  # Deskripsi wajib diisi
    image: str = Field(..., description="URL gambar program")  # URL gambar wajib diisi
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Waktu pembuatan")  # Timestamp otomatis

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,  # Izinkan pengisian berdasarkan nama
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "title": "Workshop Data Science",
                "subtitle": "Pengenalan Data Science untuk Pemula",
                "description": "Workshop pengenalan data science untuk pemula",
                "image": "/static/uploads/program1.jpg"
            }
        }
    )

# Model response untuk Program, menambahkan id
class ProgramResponse(ProgramBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID MongoDB

    # Konfigurasi model response
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}  # Konversi ObjectId ke string saat serialisasi
    )

# Model dasar untuk Blog
class BlogBase(BaseModel):
    title: str = Field(..., min_length=3, description="Judul blog")  # Judul wajib diisi, min 3 karakter
    content: str = Field(..., description="Konten blog")  # Konten wajib diisi
    image: str = Field(..., description="URL gambar blog")  # URL gambar wajib diisi
    author: str = Field(..., description="Email pembuat blog")  # Email author wajib diisi
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Waktu pembuatan")  # Timestamp otomatis

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "title": "Pengenalan Data Science",
                "content": "Data science adalah...",
                "image": "/static/uploads/blog1.jpg",
                "author": "admin@example.com"
            }
        }
    )

# Model response untuk Blog, menambahkan id
class BlogResponse(BlogBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID MongoDB

    # Konfigurasi model response
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}  # Konversi ObjectId ke string saat serialisasi
    )

# Model dasar untuk Gallery
class GalleryBase(BaseModel):
    title: Optional[str] = Field(None, description="Judul foto")  # Judul opsional
    description: Optional[str] = Field(None, description="Deskripsi foto")  # Deskripsi opsional
    image: str = Field(..., description="URL foto")  # URL foto wajib diisi
    author: str = Field(..., description="Email pengunggah foto")  # Email author wajib diisi
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Waktu unggah")  # Timestamp otomatis

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "title": "Workshop Data Science 2024",
                "description": "Dokumentasi workshop data science",
                "image": "/static/uploads/gallery1.jpg",
                "author": "admin@example.com"
            }
        }
    )

# Model response untuk Gallery, menambahkan id
class GalleryResponse(GalleryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID MongoDB

    # Konfigurasi model response
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}  # Konversi ObjectId ke string saat serialisasi
    )

# Model dasar untuk Partner
class PartnerBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nama partner/mitra")  # Nama wajib diisi, min 3 karakter
    description: Optional[str] = Field(None, min_length=10, description="Deskripsi partner/mitra")  # Deskripsi opsional, min 10 karakter
    website_url: HttpUrl = Field(..., description="URL website partner")  # URL website wajib diisi
    logo: str = Field(..., description="URL logo partner")  # URL logo wajib diisi
    author: str = Field(..., description="Email penambah partner")  # Email author wajib diisi
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Waktu penambahan")  # Timestamp otomatis

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "name": "Tech Company",
                "description": "Perusahaan teknologi terkemuka",
                "website_url": "https://example.com",
                "logo": "/static/uploads/partner1.jpg",
                "author": "admin@example.com"
            }
        }
    )

# Model response untuk Partner, menambahkan id
class PartnerResponse(PartnerBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID MongoDB

    # Konfigurasi model response
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}  # Konversi ObjectId ke string saat serialisasi
    )

# Model untuk Response Envelope (pembungkus response)
class ResponseEnvelope(BaseModel, Generic[T]):
    status: str = Field(..., description="Status response (success/error)")  # Status wajib diisi
    message: str = Field(..., description="Pesan response")  # Pesan wajib diisi
    data: Optional[T] = Field(None, description="Data response")  # Data opsional
    meta: Optional[dict] = Field(None, description="Metadata response")  # Metadata opsional

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "status": "success",
                "message": "Data berhasil diambil",
                "data": None,
                "meta": None
            }
        }
    )

# Model untuk Token autentikasi
class Token(BaseModel):
    access_token: str  # Token akses
    token_type: str  # Tipe token

    # Konfigurasi model
    model_config = ConfigDict(
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )

# Model untuk data Token
class TokenData(BaseModel):
    email: Optional[str] = None  # Email opsional
    user_id: Optional[str] = None  # ID user opsional
    username: Optional[str] = None  # Username opsional

# Model dasar untuk User
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email user")  # Email wajib diisi
    username: str = Field(..., min_length=3, description="Username untuk login")  # Username wajib diisi, min 3 karakter
    full_name: str = Field(..., min_length=3, description="Nama lengkap user")  # Nama lengkap wajib diisi, min 3 karakter
    is_active: bool = Field(default=True, description="Status aktif user")  # Status aktif default True
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Waktu pendaftaran")  # Timestamp otomatis

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True
            }
        }
    )

# Model untuk membuat User baru
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email user")  # Email wajib diisi
    username: str = Field(..., min_length=3, description="Username untuk login")  # Username wajib diisi, min 3 karakter
    full_name: str = Field(..., min_length=3, description="Nama lengkap user")  # Nama lengkap wajib diisi, min 3 karakter
    password: str = Field(..., min_length=8, description="Password user")  # Password wajib diisi, min 8 karakter

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "secretpassword"
            }
        }
    )

# Model untuk login User
class UserLogin(BaseModel):
    email: str  # Email untuk login
    password: str  # Password untuk login

    # Konfigurasi model
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={  # Contoh data untuk dokumentasi
            "example": {
                "email": "user@example.com",
                "password": "secretpassword"
            }
        }
    )

# Model response untuk User, menambahkan id
class UserResponse(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID MongoDB

    # Konfigurasi model response
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}  # Konversi ObjectId ke string saat serialisasi
    )
```

Modul Schemas ini menyediakan model-model data untuk:

1. User (registrasi, response)
2. Program (base, response)
3. Blog (base, response)
4. Gallery (base, response)
5. Partner (base, response)
6. Response Envelope untuk format response yang konsisten

Fitur utama:

- Validasi data otomatis menggunakan Pydantic
- Custom validator untuk MongoDB ObjectId
- Field dengan validasi pattern (email, program_type)
- Field dengan validasi panjang minimum
- Timestamp otomatis untuk created_at
- Response model yang konsisten untuk semua entitas
- Optional fields dengan default values
- Dokumentasi field dengan example dan description

Validasi yang diterapkan:

- Email harus valid (format standar)
- Username minimal 3 karakter
- Password minimal 6 karakter
- Program type harus salah satu dari: human_library, workshop, sosialisasi
- Title untuk semua entitas minimal 3 karakter
- ObjectId harus valid sesuai format MongoDB

### Langkah 3: Setup File Handler (file_handler.py)

1. Implementasi fungsi untuk menangani file uploads:

```python
# Import library yang diperlukan
import os  # Untuk operasi sistem file
import shutil  # Untuk operasi file tingkat tinggi
from fastapi import UploadFile, HTTPException  # Untuk handle upload file dan error
from datetime import datetime  # Untuk timestamp
import uuid  # Untuk generate ID unik

# Definisikan direktori upload dan ukuran maksimal file
UPLOAD_DIR = "static/uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Buat direktori jika belum ada
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    """
    Fungsi untuk menyimpan file yang diupload

    Args:
        file (UploadFile): File yang akan diupload

    Returns:
        str: Path file yang tersimpan

    Raises:
        HTTPException: Jika tipe file tidak diizinkan atau gagal upload
    """
    # Cek apakah file ada
    if not file:
        return None
        
    # Validasi tipe file
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Tipe file tidak diizinkan. Hanya JPEG, PNG dan GIF yang diperbolehkan"
        )
    
    # Validasi ukuran file
    try:
        file_size = 0
        while chunk := await file.read(8192):
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="Ukuran file terlalu besar. Maksimal 5MB"
                )
        await file.seek(0)  # Reset file pointer
    except Exception as e:
        if not isinstance(e, HTTPException):
            raise HTTPException(
                status_code=400,
                detail=f"Gagal memvalidasi file: {str(e)}"
            )
        raise e

    # Generate nama file unik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = os.path.splitext(file.filename)[1].lower()
    if not file_extension:
        file_extension = ".jpg"  # Default extension
    filename = f"{timestamp}_{unique_id}{file_extension}"
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Simpan file ke sistem
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal mengunggah file: {str(e)}"
        )
    finally:
        file.file.close()
    
    # Return path file yang bisa diakses
    return f"/{UPLOAD_DIR}/{filename}"
```

Modul File Handler ini menyediakan fungsi untuk menangani upload file dengan fitur:

1. Validasi File
   - Pembatasan tipe file (JPEG, PNG, GIF)
   - Pembatasan ukuran maksimal (5MB)
   - Pengecekan keberadaan file

2. Keamanan
   - Nama file yang unik dengan timestamp dan UUID
   - Validasi tipe MIME
   - Penanganan error yang aman
   - Penutupan file secara otomatis

3. Penyimpanan
   - Pembuatan direktori otomatis

### Langkah 4: Setup Config (config.py)

1. Implementasi konfigurasi aplikasi:

```python
# Import library yang diperlukan
from pydantic_settings import BaseSettings, SettingsConfigDict # Untuk pengaturan aplikasi
from decouple import config # Untuk membaca variabel environment
from typing import List # Untuk tipe data list
import os # Untuk operasi path
import json # Untuk parsing JSON

class Settings(BaseSettings):
    """Pengaturan aplikasi."""
    
    # Pengaturan API
    API_V1_STR: str = "/api/v1" # Prefix untuk API v1
    PROJECT_NAME: str = "Lembaga Sinergi Analitika API" # Nama proyek
    VERSION: str = "1.0.0" # Versi API
    DEBUG_MODE: bool = config("DEBUG_MODE", default=False, cast=bool) # Mode debug
    
    # Pengaturan MongoDB
    MONGODB_URL: str = config("MONGODB_URL") # URL koneksi MongoDB
    MONGODB_DATABASE: str = config("MONGODB_DATABASE") # Nama database utama
    MONGODB_TEST_DB: str = config("MONGODB_TEST_DB") # Nama database testing
    
    # Pengaturan JWT
    SECRET_KEY: str = config("SECRET_KEY") # Kunci rahasia untuk JWT
    ALGORITHM: str = config("ALGORITHM") # Algoritma enkripsi
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int) # Waktu kadaluarsa token
    
    # Pengaturan CORS
    ALLOWED_ORIGINS: List[str] = json.loads(config("ALLOWED_ORIGINS")) # Domain yang diizinkan
    
    # Pengaturan Upload File
    STATIC_DIR: str = "static" # Direktori file statis
    UPLOAD_DIR: str = os.path.join("static", "uploads") # Direktori upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # Ukuran maksimal file (5MB)
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif"] # Tipe file yang diizinkan
    
    # Pengaturan Admin
    ADMIN_EMAIL: str = config("ADMIN_EMAIL") # Email admin
    ADMIN_USERNAME: str = config("ADMIN_USERNAME") # Username admin  
    ADMIN_PASSWORD: str = config("ADMIN_PASSWORD") # Password admin
    
    # Konfigurasi model
    model_config = SettingsConfigDict(
        case_sensitive=True, # Case sensitive
        env_file=".env", # File environment
        env_file_encoding="utf-8", # Encoding file
        extra="allow" # Izinkan field tambahan
    )

# Inisialisasi pengaturan
settings = Settings()
```

Modul Config ini menyediakan konfigurasi aplikasi dengan fitur:

1. Pengaturan API
2. Pengaturan MongoDB
3. Pengaturan JWT
4. Pengaturan CORS
5. Pengaturan Upload File
6. Pengaturan Admin

Fitur utama:

- Konfigurasi dengan pydantic settings
- Pengaturan dari environment variable
- Validasi konfigurasi dengan pydantic
- Dokumentasi konfigurasi dengan example

Keamanan:

- Konfigurasi dari environment variable
- Validasi konfigurasi dengan pydantic
- Dokumentasi konfigurasi dengan example

### Langkah 5: Setup Security (security.py)

1. Implementasi fungsi untuk keamanan JWT:

```python
# Import library yang diperlukan
from datetime import datetime, timedelta  # Untuk menangani tanggal dan waktu
from typing import Optional  # Untuk tipe data opsional
from jose import JWTError, jwt  # Untuk pemrosesan JWT token
from passlib.context import CryptContext  # Untuk hashing password
from app.core.config import settings  # Import pengaturan aplikasi

# Inisialisasi context untuk password hashing menggunakan bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],  # Menggunakan algoritma bcrypt
    deprecated="auto",   # Otomatis menangani skema yang sudah usang
    bcrypt__rounds=12    # Jumlah putaran hashing
)

# Fungsi untuk memverifikasi password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Verifikasi password plain dengan hash
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Jika terjadi error, cetak pesan error dan return False
        print(f"Password verification error: {str(e)}")
        return False

# Fungsi untuk menghasilkan hash dari password (untuk registrasi)
def get_password_hash(password: str) -> str:
    try:
        # Generate hash dari password
        return pwd_context.hash(password)
    except Exception as e:
        # Jika terjadi error, cetak pesan dan raise exception
        print(f"Password hashing error: {str(e)}")
        raise

# Fungsi untuk membuat token akses JWT (untuk login)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Buat salinan data yang akan dienkripsi
    to_encode = data.copy()
    if expires_delta:
        # Jika ada waktu kadaluarsa, tambahkan ke waktu sekarang
        expire = datetime.utcnow() + expires_delta
    else:
        # Jika tidak ada, gunakan 15 menit sebagai default
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Tambahkan waktu kadaluarsa ke data
    to_encode.update({"exp": expire})
    # Encode data menjadi JWT token
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
```

Modul Security ini menyediakan fungsi untuk:

1. Verifikasi password
2. Hashing password
3. Membuat JWT token

Fitur utama:

- Verifikasi password dengan bcrypt
- Membuat JWT token dengan HS256
- Waktu kadaluarsa token dari konfigurasi
- Validasi token dengan JWTError

Keamanan:

- Verifikasi password dengan bcrypt
- Membuat JWT token dengan HS256
- Waktu kadaluarsa token dari konfigurasi
- Validasi token dengan JWTError

## TAHAP 2: IMPLEMENTASI AUTHENTICATION

### Langkah 1: Setup Dependencies (deps.py)

1. Implementasi dependency untuk authentication:

```python
# Import library yang diperlukan
from fastapi import Depends, HTTPException, status  # Untuk dependency injection dan penanganan error
from fastapi.security import OAuth2PasswordBearer  # Untuk implementasi autentikasi OAuth2
from jose import jwt, JWTError  # Untuk pemrosesan JWT token
from app.models.schemas import TokenData  # Model data token
from app.core.database import get_database  # Koneksi database
from app.core.config import settings  # Pengaturan aplikasi

# Inisialisasi OAuth2 dengan endpoint login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Fungsi untuk mendapatkan data user yang sedang login
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    # Exception untuk kredensial tidak valid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kredensial tidak valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    # Cek user di database
    user = await db.users.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user

# Fungsi untuk memastikan user aktif
async def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.get("is_active", False):
        raise HTTPException(status_code=400, detail="User tidak aktif")
    return current_user
```

### Langkah 2: Implementasi Authentication Endpoints

1. Buat file auth.py di app/api/endpoints/
2. Implementasi login dan register

```python
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends, status # Import FastAPI dan komponen yang dibutuhkan
from fastapi.security import OAuth2PasswordRequestForm # Import form untuk login OAuth2
from app.models.schemas import UserCreate, UserLogin, ResponseEnvelope, Token # Import model data
from app.core.security import create_access_token, verify_password, get_password_hash # Import fungsi keamanan
from app.core.database import get_database # Import koneksi database
from app.core.config import settings # Import konfigurasi aplikasi
from datetime import timedelta # Import untuk menangani waktu
from fastapi.responses import JSONResponse # Import untuk response JSON
import logging # Import untuk logging

router = APIRouter() # Inisialisasi router FastAPI
logger = logging.getLogger(__name__) # Inisialisasi logger

@router.post("/register", response_model=ResponseEnvelope, status_code=201) # Endpoint untuk registrasi
async def register(user: UserCreate, db=Depends(get_database)): # Fungsi registrasi dengan parameter user dan database
    # Cek apakah email sudah terdaftar di database
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        return JSONResponse( # Jika email sudah ada, kirim response error
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error", 
                "message": "Email already registered",
                "data": None,
                "meta": None
            }
        )

    # Cek apakah username sudah digunakan
    existing_username = await db.users.find_one({"username": user.username})
    if existing_username:
        return JSONResponse( # Jika username sudah ada, kirim response error
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "message": "Username already taken", 
                "data": None,
                "meta": None
            }
        )

    # Hash password sebelum disimpan ke database
    hashed_password = get_password_hash(user.password)

    # Siapkan data user untuk disimpan
    user_data = {
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "password": hashed_password,
        "is_active": True
    }

    # Simpan user baru ke database
    result = await db.users.insert_one(user_data)

    # Siapkan data user untuk response (tanpa password)
    user_response = {
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "is_active": True,
        "id": str(result.inserted_id)
    }

    # Kirim response sukses
    return ResponseEnvelope(
        status="success",
        message="User registered successfully",
        data=user_response,
        meta=None
    )

@router.post("/login", response_model=Token) # Endpoint untuk login
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)): # Fungsi login dengan form data dan database
    try:
        username = form_data.username.lower().strip() # Normalisasi username

        # Cari user di database berdasarkan email atau username
        db_user = await db.users.find_one({
            "$or": [
                {"email": username},
                {"username": username}
            ]
        })

        # Jika user tidak ditemukan, kirim error
        if not db_user:
            logger.warning(f"User not found: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Verifikasi password yang diinput
        if not verify_password(form_data.password, db_user["password"]):
            logger.warning(f"Invalid password for user: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Generate access token untuk user yang berhasil login
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": db_user["email"],
                "user_id": str(db_user["_id"]),
                "username": db_user["username"]
            },
            expires_delta=access_token_expires
        )

        # Kirim response dengan access token
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

Modul Authentication ini menyediakan endpoint-endpoint untuk:

1. Registrasi user baru dengan email, username, dan password
2. Login user dengan email dan password untuk mendapatkan access token

Fitur utama:

- Password hashing menggunakan bcrypt
- JWT (JSON Web Token) untuk autentikasi
- Validasi email unik saat registrasi
- Status aktif/non-aktif untuk user
- Role admin/non-admin
- Token expiry time 30 menit
- Error handling untuk berbagai kasus login/register

Keamanan:

- Password tidak pernah disimpan dalam bentuk plain text
- Token menggunakan algoritma HS256
- Secret key dari environment variable
- Pesan error yang aman (tidak mengungkapkan detail teknis)
- Validasi status user saat login

## TAHAP 3: IMPLEMENTASI CORE MODULES

### Langkah 1: Programs Module

1. Buat file programs.py di app/api/endpoints/:

```python
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query, status
from fastapi.responses import JSONResponse
from app.models.schemas import ProgramBase, ProgramResponse, ResponseEnvelope
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List, Literal, Union, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from enum import Enum

# Definisi enum untuk tipe program
class ProgramType(str, Enum):
    ALL = "all"  # Untuk filter semua program
    HUMAN_LIBRARY = "human_library"  # Program Human Library
    WORKSHOP = "workshop"  # Program Workshop
    SOSIALISASI = "sosialisasi"  # Program Sosialisasi
    SEMINAR = "seminar"  # Program Seminar
    TRAINING = "training"  # Program Training

# Inisialisasi router dengan tag programs
router = APIRouter(tags=["programs"])

# Fungsi untuk mengkonversi ObjectId ke string
def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# Endpoint untuk membuat program baru
@router.post(
    "", 
    response_model=ResponseEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Membuat Program Baru",
    description="""
    Membuat program baru dengan gambar.
    
    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    
    **Tipe Program yang Tersedia:**
    - human_library: Program Human Library
    - workshop: Program Workshop
    - sosialisasi: Program Sosialisasi
    - seminar: Program Seminar
    - training: Program Training
    """
)
async def create_program(
    title: str = Form(..., description="Judul program", examples=["Workshop Pemulihan Mental"]),
    description: str = Form(..., description="Deskripsi program", examples=["Workshop untuk pemulihan kesehatan mental..."]),
    program_type: ProgramType = Form(
        ..., 
        description="Tipe program (human_library, workshop, sosialisasi, seminar, training)",
        exclude=["ALL"]
    ),
    image: UploadFile = File(
        ..., 
        description="File gambar untuk program (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    start_date: datetime = Form(..., description="Tanggal mulai program", examples=["2024-01-01T00:00:00"]),
    end_date: datetime = Form(..., description="Tanggal selesai program", examples=["2024-01-02T00:00:00"]),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload gambar
    image_url = await save_upload_file(image)

    # Menyiapkan data program
    program_data = {
        "title": title,
        "description": description,
        "program_type": program_type.value,
        "image": image_url,
        "start_date": start_date,
        "end_date": end_date,
        "is_active": True,
        "author": current_user["email"],
        "created_at": datetime.utcnow()
    }
    
    # Validasi data program menggunakan ProgramBase
    program = ProgramBase(**program_data)
    
    # Menyimpan program ke database
    result = await db.programs.insert_one(program.model_dump())
    created_program = await db.programs.find_one({"_id": result.inserted_id})
    created_program = convert_objectid(created_program)
    
    return ResponseEnvelope(
        status="success",
        message="Program berhasil dibuat",
        data=created_program
    )

# Endpoint untuk mendapatkan daftar program
@router.get(
    "", 
    response_model=ResponseEnvelope,
    summary="Mengambil Semua Program",
    description="""
    Mengambil daftar program yang tersedia.
    
    **Filter Tipe Program:**
    - all: Menampilkan semua program
    - human_library: Hanya program human library
    - workshop: Hanya program workshop
    - sosialisasi: Hanya program sosialisasi
    - seminar: Hanya program seminar
    - training: Hanya program training
    """
)
async def get_programs(
    program_type: ProgramType = Query(
        ProgramType.ALL,
        description="Filter berdasarkan tipe program"
    ),
    db=Depends(get_database)
):
    # Menyiapkan query filter
    query = {}
    if program_type != ProgramType.ALL:
        query["program_type"] = program_type.value
        
    # Mengambil data program dari database
    programs = await db.programs.find(query).to_list(1000)
    programs = [convert_objectid(program) for program in programs]
    
    return ResponseEnvelope(
        status="success",
        message="Daftar program berhasil diambil",
        data=programs
    )

# Endpoint untuk mendapatkan detail program
@router.get(
    "/{program_id}", 
    response_model=ResponseEnvelope,
    summary="Mengambil Detail Program",
    description="Mengambil detail program berdasarkan ID."
)
async def get_program(program_id: str, db=Depends(get_database)):
    # Validasi format ID
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        error_response = ResponseEnvelope(
            status="error",
            message="ID program tidak valid. ID harus berupa 24 karakter hex string.",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    # Mencari program di database
    program = await db.programs.find_one({"_id": object_id})
    if not program:
        error_response = ResponseEnvelope(
            status="error",
            message="Program tidak ditemukan",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )
    
    program = convert_objectid(program)
    return ResponseEnvelope(
        status="success",
        message="Detail program berhasil diambil",
        data=program
    )

# Endpoint untuk menghapus program
@router.delete(
    "/{program_id}",
    response_model=ResponseEnvelope,
    summary="Menghapus Program",
    description="Menghapus program berdasarkan ID."
)
async def delete_program(
    program_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Validasi format ID
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        error_response = ResponseEnvelope(
            status="error",
            message="ID program tidak valid. ID harus berupa 24 karakter hex string.",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    # Menghapus program dari database
    result = await db.programs.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        error_response = ResponseEnvelope(
            status="error",
            message="Program tidak ditemukan",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )
    
    return ResponseEnvelope(
        status="success",
        message="Program berhasil dihapus",
        data=None
    )
```

Modul Programs ini menyediakan endpoint-endpoint untuk:

1. Membuat program baru dengan data dari request body
2. Mendapatkan daftar semua program
3. Mendapatkan detail program berdasarkan ID
4. Menghapus program berdasarkan ID

Fitur utama:

- Validasi data menggunakan Pydantic models (ProgramBase)
- Autentikasi wajib untuk operasi create dan delete
- Konversi otomatis antara ObjectId MongoDB dan string
- Error handling untuk kasus program tidak ditemukan
- Response model yang konsisten (ProgramResponse)

Catatan penting:

- Batasan 1000 item untuk daftar program
- Menggunakan model_dump() untuk konversi Pydantic model ke dict (ProgramBase)
- Autentikasi menggunakan dependency get_current_user
- Penggunaan ObjectId untuk operasi database

### Langkah 2: Blog Module

1. Buat file blog.py di app/api/endpoints/:

```python
# Import library yang diperlukan
from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, UploadFile, File  # Import FastAPI dan komponen yang dibutuhkan
from fastapi.responses import JSONResponse  # Import untuk response JSON
from typing import List, Dict, Any  # Import tipe data untuk list, dictionary dan any
from bson import ObjectId  # Import ObjectId untuk MongoDB
from datetime import datetime  # Import datetime untuk timestamp
from app.core.database import get_database  # Import koneksi database
from app.models.schemas import BlogBase, BlogResponse, ResponseEnvelope  # Import model data
from app.api.deps import get_current_user  # Import fungsi untuk mendapatkan user yang sedang login
from app.utils.file_handler import save_upload_file  # Import fungsi untuk menyimpan file

router = APIRouter()  # Inisialisasi router FastAPI

# Fungsi untuk mengkonversi ObjectId menjadi string
def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Mengkonversi ObjectId menjadi string dalam dokumen"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# Endpoint untuk membuat blog baru
@router.post("", response_model=ResponseEnvelope[BlogResponse], status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: str = Form(...),  # Parameter judul dari form
    content: str = Form(...),  # Parameter konten dari form 
    image: UploadFile = File(...),  # Parameter file gambar
    current_user=Depends(get_current_user),  # Mendapatkan user yang sedang login
    db=Depends(get_database)  # Mendapatkan koneksi database
):
    """Membuat blog baru"""
    try:
        # Menyimpan gambar jika ada
        image_path = await save_upload_file(image)

        # Menyiapkan data blog
        blog_data = {
            "title": title,
            "content": content, 
            "image": image_path,
            "author": current_user["email"],
            "created_at": datetime.utcnow()
        }

        # Menyimpan blog ke database
        result = await db["blogs"].insert_one(blog_data)

        # Mendapatkan blog yang baru dibuat
        created_blog = await db["blogs"].find_one({"_id": result.inserted_id})
        created_blog = convert_objectid(created_blog)

        # Mengembalikan response sukses
        return ResponseEnvelope[BlogResponse](
            status="success",
            message="Blog berhasil dibuat",
            data=created_blog
        )

    except Exception as e:
        # Menangani error
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

# Endpoint untuk mendapatkan daftar blog
@router.get("", response_model=ResponseEnvelope[List[BlogResponse]])
async def get_blogs(
    db=Depends(get_database),
    skip: int = 0,  # Parameter untuk pagination
    limit: int = 10  # Parameter untuk membatasi jumlah data
):
    """Mendapatkan semua blog dengan pagination"""
    try:
        # Mengurutkan berdasarkan created_at descending (terbaru dulu)
        sort_query = [("created_at", -1)]

        # Mengambil data blog dari database
        blogs = await db["blogs"].find() \
            .sort(sort_query) \
            .skip(skip) \
            .limit(limit) \
            .to_list(None)

        # Mengkonversi ObjectId menjadi string
        blogs = [convert_objectid(blog) for blog in blogs]

        # Mengembalikan response sukses
        return ResponseEnvelope[List[BlogResponse]](
            status="success",
            message="Daftar blog berhasil diambil",
            data=blogs
        )

    except Exception as e:
        # Menangani error
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

# Endpoint untuk mendapatkan detail blog
@router.get("/{blog_id}", response_model=ResponseEnvelope[BlogResponse])
async def get_blog(blog_id: str, db=Depends(get_database)):
    """Mendapatkan blog berdasarkan ID"""
    try:
        # Validasi ID blog
        if not ObjectId.is_valid(blog_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID blog tidak valid"
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response.model_dump()
            )

        # Mencari blog di database
        blog = await db["blogs"].find_one({"_id": ObjectId(blog_id)})
        if not blog:
            error_response = ResponseEnvelope(
                status="error",
                message="Blog tidak ditemukan"
            )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=error_response.model_dump()
            )

        # Mengkonversi ObjectId menjadi string
        blog = convert_objectid(blog)
        return ResponseEnvelope[BlogResponse](
            status="success",
            message="Detail blog berhasil diambil",
            data=blog
        )

    except Exception as e:
        # Menangani error
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

# Endpoint untuk menghapus blog
@router.delete("/{blog_id}", response_model=ResponseEnvelope)
async def delete_blog(blog_id: str, current_user=Depends(get_current_user), db=Depends(get_database)):
    """Menghapus blog"""
    try:
        # Validasi ID blog
        if not ObjectId.is_valid(blog_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID blog tidak valid"
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response.model_dump()
            )

        # Mencari blog di database
        blog = await db["blogs"].find_one({"_id": ObjectId(blog_id)})
        if not blog:
            error_response = ResponseEnvelope(
                status="error",
                message="Blog tidak ditemukan"
            )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=error_response.model_dump()
            )

        # Memeriksa apakah user adalah penulis blog
        if blog["author"] != current_user["email"]:
            error_response = ResponseEnvelope(
                status="error",
                message="Anda tidak memiliki akses untuk menghapus blog ini"
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=error_response.model_dump()
            )

        # Menghapus blog dari database
        await db["blogs"].delete_one({"_id": ObjectId(blog_id)})
        return ResponseEnvelope(
            status="success",
            message="Blog berhasil dihapus"
        )

    except Exception as e:
        # Menangani error
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )
```

Modul Blog ini menyediakan endpoint-endpoint untuk:

1. Membuat blog baru dengan judul, konten, dan gambar opsional
2. Mendapatkan daftar blog dengan fitur:
   - Paginasi (skip & limit)
   - Pencarian di judul dan konten
   - Metadata (total, has_more, dll)
3. Mendapatkan detail blog berdasarkan ID
4. Menghapus blog berdasarkan ID

Fitur utama:

- Upload gambar opsional untuk blog
- Paginasi dan pencarian untuk daftar blog
- Response envelope dengan metadata
- Logging untuk monitoring dan debugging
- Autentikasi wajib untuk operasi create dan delete
- Validasi data menggunakan Pydantic models
- Error handling untuk berbagai kasus

### Langkah 3: Gallery Module

1. Implementasi gallery.py di app/api/endpoints/:

```python
# Import library yang diperlukan untuk modul gallery
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, status  # Import FastAPI dan komponen yang dibutuhkan
from fastapi.responses import JSONResponse  # Import untuk response JSON
from app.models.schemas import GalleryBase, GalleryResponse, ResponseEnvelope  # Import model data galeri
from app.core.database import get_database  # Import koneksi database
from app.api.deps import get_current_active_user, get_current_user  # Import fungsi untuk mendapatkan user yang sedang login
from app.utils.file_handler import save_upload_file  # Import fungsi untuk menyimpan file
from app.core.config import settings  # Import konfigurasi aplikasi
from typing import List, Dict, Any  # Import tipe data untuk list, dictionary dan any
from datetime import datetime  # Import datetime untuk timestamp
from bson import ObjectId  # Import ObjectId untuk MongoDB
import os  # Import os untuk operasi file system

# Inisialisasi router FastAPI dengan tag gallery
router = APIRouter(tags=["gallery"])

# Fungsi untuk mengkonversi ObjectId menjadi string
def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Mengkonversi ObjectId menjadi string dalam dokumen"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# Endpoint untuk membuat galeri baru
@router.post(
    "", 
    response_model=ResponseEnvelope[GalleryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Menambahkan Foto ke Galeri",
    description="""
    Menambahkan foto baru ke galeri.
    
    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
# Fungsi untuk membuat galeri baru dengan parameter yang diperlukan
async def create_gallery(
    title: str = Form(None, description="Judul foto", examples=["Workshop Batch 2023"]),  # Parameter judul opsional
    description: str = Form(None, description="Deskripsi foto", examples=["Dokumentasi kegiatan workshop..."]),  # Parameter deskripsi opsional
    image: UploadFile = File(  # Parameter file gambar wajib
        ..., 
        description="File foto (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),  # Mendapatkan koneksi database
    current_user=Depends(get_current_active_user)  # Mendapatkan user yang sedang login
):
    try:
        # Upload gambar dan dapatkan URL-nya
        image_url = await save_upload_file(image)
        
        # Menyiapkan data galeri untuk disimpan
        gallery_data = {
            "title": title or "",
            "description": description or "",
            "image": image_url,
            "created_at": datetime.utcnow(),
            "author": current_user["email"]
        }
        
        # Menyimpan data galeri ke database
        result = await db.gallery.insert_one(gallery_data)
        created_gallery = await db.gallery.find_one({"_id": result.inserted_id})
        created_gallery = convert_objectid(created_gallery)
        
        # Mengembalikan response sukses
        return ResponseEnvelope[GalleryResponse](
            status="success",
            message="Foto berhasil ditambahkan",
            data=created_gallery
        )
    except Exception as e:
        # Menangani error jika terjadi
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

# Endpoint untuk mendapatkan semua foto galeri
@router.get(
    "", 
    response_model=ResponseEnvelope[List[GalleryResponse]],
    summary="Mengambil Semua Foto Galeri",
    description="Mengambil daftar semua foto yang ada di galeri."
)
async def get_galleries(db=Depends(get_database)):
    try:
        # Mengambil semua data galeri dari database
        galleries = await db.gallery.find().to_list(1000)
        galleries = [convert_objectid(gallery) for gallery in galleries]
        
        # Mengembalikan response sukses
        return ResponseEnvelope[List[GalleryResponse]](
            status="success",
            message="Daftar foto berhasil diambil",
            data=galleries
        )
    except Exception as e:
        # Menangani error jika terjadi
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

# Endpoint untuk mendapatkan detail foto berdasarkan ID
@router.get("/{gallery_id}", response_model=ResponseEnvelope)
async def get_gallery(gallery_id: str, db = Depends(get_database)):
    """Mengambil detail foto berdasarkan ID"""
    try:
        # Validasi ID galeri
        if not ObjectId.is_valid(gallery_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID foto tidak valid",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_response.dict())

        # Mencari foto di database
        gallery = await db.gallery.find_one({"_id": ObjectId(gallery_id)})
        if not gallery:
            error_response = ResponseEnvelope(
                status="error",
                message="Foto tidak ditemukan",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_response.model_dump())

        # Konversi ObjectId dan kembalikan response sukses
        gallery = convert_objectid(gallery)
        return ResponseEnvelope(
            status="success",
            message="Detail foto berhasil diambil",
            data=gallery
        )
    except Exception as e:
        # Menangani error jika terjadi
        error_response = ResponseEnvelope(
            status="error",
            message=str(e),
            data=None
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.dict())

# Endpoint untuk menghapus foto berdasarkan ID
@router.delete("/{gallery_id}", response_model=ResponseEnvelope)
async def delete_gallery(gallery_id: str, current_user = Depends(get_current_user), db = Depends(get_database)):
    """Menghapus foto berdasarkan ID"""
    try:
        # Validasi ID galeri
        if not ObjectId.is_valid(gallery_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID foto tidak valid",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_response.dict())

        # Mencari foto di database
        gallery = await db.gallery.find_one({"_id": ObjectId(gallery_id)})
        if not gallery:
            error_response = ResponseEnvelope(
                status="error",
                message="Foto tidak ditemukan",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_response.model_dump())

        # Hapus file foto dari sistem file
        if gallery.get("image"):
            image_path = os.path.join(settings.STATIC_DIR, gallery["image"].lstrip("/static/"))
            if os.path.exists(image_path):
                os.remove(image_path)

        # Hapus data dari database
        await db.gallery.delete_one({"_id": ObjectId(gallery_id)})

        # Kembalikan response sukses
        return ResponseEnvelope(
            status="success",
            message="Foto berhasil dihapus",
            data=None
        )
    except Exception as e:
        # Menangani error jika terjadi
        error_response = ResponseEnvelope(
            status="error",
            message=str(e),
            data=None
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.dict())
```

Modul Gallery ini menyediakan endpoint-endpoint untuk:

1. Membuat galeri baru dengan judul, deskripsi, dan gambar wajib
2. Mendapatkan daftar semua galeri
3. Mendapatkan detail galeri berdasarkan ID
4. Menghapus galeri berdasarkan ID

Fitur utama:

- Upload gambar wajib untuk setiap galeri
- Autentikasi wajib untuk operasi create dan delete
- Validasi data menggunakan Pydantic models
- Error handling untuk kasus galeri tidak ditemukan
- Timestamp otomatis saat pembuatan galeri

### Langkah 4: Partners Module

1. Buat file partners.py di app/api/endpoints/:

```python
# Import library yang diperlukan untuk modul partners
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, logger, status  # Import FastAPI dan komponen yang dibutuhkan
from fastapi.responses import JSONResponse  # Import untuk response JSON
from app.models.schemas import PartnerBase, PartnerResponse, ResponseEnvelope  # Import model data partner
from app.core.database import get_database  # Import koneksi database
from app.api.deps import get_current_active_user  # Import fungsi untuk mendapatkan user aktif
from app.utils.file_handler import save_upload_file  # Import fungsi untuk menyimpan file
from app.core.config import settings  # Import konfigurasi aplikasi
from typing import List, Dict, Any  # Import tipe data untuk list, dictionary dan any
from datetime import datetime  # Import datetime untuk timestamp
from bson import ObjectId  # Import ObjectId untuk MongoDB
import os  # Import os untuk operasi file system

# Inisialisasi router FastAPI dengan tag partners
router = APIRouter(tags=["partners"])

# Fungsi untuk mengkonversi ObjectId menjadi string
def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Mengkonversi ObjectId menjadi string dalam dokumen"""
    if doc and "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

# Endpoint untuk membuat partner baru
@router.post(
    "", 
    response_model=ResponseEnvelope[PartnerResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Menambahkan Partner Baru",
    description="""
    Menambahkan partner/mitra baru dengan logo.
    
    **Format Logo yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
# Fungsi untuk membuat partner baru dengan parameter yang diperlukan
async def create_partner(
    name: str = Form(..., description="Nama partner/mitra", examples=["Universitas Indonesia"]),  # Parameter nama wajib
    description: str = Form(None, description="Deskripsi partner/mitra", examples=["Mitra dalam penyelenggaraan workshop..."]),  # Parameter deskripsi opsional
    website_url: str = Form(..., description="URL website partner", examples=["https://www.ui.ac.id"]),  # Parameter URL website wajib
    logo: UploadFile = File(  # Parameter file logo wajib
        ..., 
        description="File logo partner (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),  # Mendapatkan koneksi database
    current_user=Depends(get_current_active_user)  # Mendapatkan user yang sedang login
):
    # Validasi URL website
    try:
        from pydantic import HttpUrl
        HttpUrl(website_url)
    except:
        error_response = ResponseEnvelope(
            status="error",
            message="URL website tidak valid. Harap masukkan URL yang valid (contoh: https://www.example.com)"
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.model_dump()
        )
    
    # Upload logo dan dapatkan URL-nya
    logo_url = await save_upload_file(logo)
    
    # Menyiapkan data partner untuk disimpan
    partner_data = {
        "name": name,
        "description": description or "",
        "website_url": website_url,
        "logo": logo_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }
    
    # Menyimpan data partner ke database
    result = await db.partners.insert_one(partner_data)
    created_partner = await db.partners.find_one({"_id": result.inserted_id})
    created_partner = convert_objectid(created_partner)
    
    # Mengembalikan response sukses
    return ResponseEnvelope(
        status="success",
        message="Partner berhasil ditambahkan",
        data=created_partner
    )

# Endpoint untuk mendapatkan semua partner
@router.get(
    "", 
    response_model=ResponseEnvelope[List[PartnerResponse]],
    summary="Mengambil Semua Partner",
    description="Mengambil daftar semua partner/mitra."
)
async def get_partners(db=Depends(get_database)):
    # Mengambil semua partner dari database
    partners = await db.partners.find().to_list(1000)
    partners = [convert_objectid(partner) for partner in partners]
    
    # Mengembalikan response sukses
    return ResponseEnvelope(
        status="success",
        message="Daftar partner berhasil diambil",
        data=partners
    )

# Endpoint untuk mendapatkan detail partner berdasarkan ID
@router.get(
    "/{partner_id}", 
    response_model=ResponseEnvelope[PartnerResponse],
    summary="Mengambil Detail Partner",
    description="Mengambil detail partner/mitra berdasarkan ID."
)
async def get_partner(partner_id: str, db=Depends(get_database)):
    # Validasi format ID partner
    if not ObjectId.is_valid(partner_id):
        error_response = ResponseEnvelope(
            status="error",
            message="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    # Mencari partner berdasarkan ID    
    partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
    if not partner:
        error_response = ResponseEnvelope(
            status="error",
            message="Partner tidak ditemukan"
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )
    
    # Mengkonversi ObjectId dan mengembalikan response sukses
    partner = convert_objectid(partner)
    return ResponseEnvelope(
        status="success",
        message="Detail partner berhasil diambil",
        data=partner
    )

# Endpoint untuk menghapus partner berdasarkan ID
@router.delete(
    "/{partner_id}",
    response_model=ResponseEnvelope,
    summary="Menghapus Partner",
    description="Menghapus partner/mitra berdasarkan ID."
)
async def delete_partner(
    partner_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Validasi format ID partner
    if not ObjectId.is_valid(partner_id):
        error_response = ResponseEnvelope(
            status="error",
            message="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    # Mencari partner berdasarkan ID
    partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
    if not partner:
        error_response = ResponseEnvelope(
            status="error",
            message="Partner tidak ditemukan"
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )
    
    # Menghapus file logo jika ada
    if partner.get("logo"):
        try:
            logo_path = os.path.join(settings.STATIC_DIR, partner["logo"].lstrip("/static/"))
            if os.path.exists(logo_path):
                os.remove(logo_path)
        except Exception as e:
            logger.error(f"Error deleting logo file: {str(e)}")
    
    # Menghapus data partner dari database
    await db.partners.delete_one({"_id": ObjectId(partner_id)})
    
    # Mengembalikan response sukses
    return ResponseEnvelope(
        status="success",
        message="Partner berhasil dihapus"
    )
```

Modul Partners ini menyediakan endpoint-endpoint untuk:

1. Membuat partner baru dengan informasi nama, deskripsi, URL website, dan logo
2. Mendapatkan daftar semua partner
3. Mendapatkan detail partner berdasarkan ID
4. Menghapus partner berdasarkan ID

Fitur utama:

- Upload logo partner dengan validasi file
- Autentikasi wajib untuk operasi create dan delete
- Validasi data menggunakan Pydantic models
- Error handling untuk kasus partner tidak ditemukan

## TAHAP 4: SETUP MAIN APPLICATION

### Langkah 1: Implementasi Main App

1. Edit main.py di root folder:

```python
# Import library yang diperlukan
from fastapi import FastAPI, Request, Depends  # Import FastAPI dan komponen yang dibutuhkan untuk aplikasi web
from fastapi.middleware.cors import CORSMiddleware  # Import middleware untuk menangani CORS (Cross Origin Resource Sharing)
from app.core.database import connect_to_mongo, close_mongo_connection  # Import fungsi untuk koneksi ke MongoDB
from app.api.endpoints import programs, auth, blog, gallery, partners  # Import semua router endpoint API
import uvicorn  # Import server ASGI untuk menjalankan aplikasi FastAPI
from fastapi.staticfiles import StaticFiles  # Import untuk melayani file statis (gambar, css, dll)
from decouple import config  # Import untuk membaca variabel environment
import uuid  # Import untuk menghasilkan ID unik
import logging  # Import untuk mencatat log aplikasi
from fastapi.security import OAuth2PasswordBearer  # Import untuk implementasi autentikasi OAuth2

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)  # Set level logging ke INFO
logger = logging.getLogger(__name__)  # Buat instance logger

# Muat variabel environment
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)  # Ambil mode debug dari env
ALLOWED_ORIGINS = config("ALLOWED_ORIGINS", default="*").split(",")  # Ambil origins yang diizinkan untuk CORS

# Konfigurasi OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Set endpoint untuk login OAuth2

# Inisialisasi aplikasi FastAPI dengan metadata
app = FastAPI(
    title="Lembaga Sinergi Analitika API",  # Judul API
    description="API untuk mengelola program, blog, galeri, dan mitra Lembaga Sinergi Analitika",  # Deskripsi API
    version="1.0.0",  # Versi API
    openapi_tags=[  # Definisi tag untuk pengelompokan endpoint
        {
            "name": "authentication",
            "description": "Operasi terkait autentikasi pengguna"
        },
        {
            "name": "programs", 
            "description": "Operasi CRUD untuk program dan kegiatan"
        },
        {
            "name": "blogs",
            "description": "Endpoint untuk manajemen blog dan artikel"
        },
        {
            "name": "gallery",
            "description": "Endpoint untuk manajemen galeri foto"
        },
        {
            "name": "partners",
            "description": "Endpoint untuk manajemen mitra/partner"
        }
    ]
)

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Origins yang diizinkan
    allow_credentials=True,  # Izinkan credentials
    allow_methods=["*"],  # Izinkan semua method HTTP
    allow_headers=["*"],  # Izinkan semua header
)

# Middleware untuk menambahkan ID unik ke setiap request
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())  # Generate ID unik
    request.state.request_id = request_id  # Simpan ID di state request
    response = await call_next(request)  # Proses request
    response.headers["X-Request-ID"] = request_id  # Tambahkan ID ke header response
    return response

# Mount direktori static untuk file statis
app.mount("/static", StaticFiles(directory="static"), name="static")

# Daftarkan event handler
app.add_event_handler("startup", connect_to_mongo)  # Koneksi ke MongoDB saat startup
app.add_event_handler("shutdown", close_mongo_connection)  # Tutup koneksi saat shutdown

# Daftarkan semua router
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(programs.router, prefix="/programs", tags=["programs"])
app.include_router(blog.router, prefix="/blogs", tags=["blogs"])
app.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
app.include_router(partners.router, prefix="/partners", tags=["partners"])

# Konfigurasi Swagger UI untuk OAuth2
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": "",
    "clientSecret": ""
}

# Entry point aplikasi
if __name__ == "__main__":
    uvicorn.run(  # Jalankan server dengan uvicorn
        "app.main:app",  # Path ke aplikasi
        host="0.0.0.0",  # Host yang digunakan
        port=8000,  # Port yang digunakan
        reload=DEBUG_MODE  # Auto-reload jika dalam mode debug
    )
```

### Langkah 2: Setup Database Seeder

1. Implementasi seeder.py:

```python
# Import library yang diperlukan
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from decouple import config
from datetime import datetime
from app.core.security import get_password_hash

# Fungsi utama untuk melakukan seeding data
async def seed_all():
    client = None
    try:
        # Ambil konfigurasi database dari environment variables
        MONGODB_URL = config("MONGODB_URL").split('#')[0].strip()  # type: ignore
        DATABASE_NAME = config("MONGODB_DATABASE").split('#')[0].strip()  # type: ignore

        print(f"Nama database: '{DATABASE_NAME}'")  # Debug line dengan quotes

        # Buat koneksi ke MongoDB dengan konfigurasi timeout
        print("Menghubungkan ke database...")
        client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxIdleTimeMS=30000
        )

        # Tes koneksi ke database
        await client.admin.command('ping')
        print("Berhasil terhubung ke MongoDB.")

        # Reset database yang ada
        await client.drop_database(DATABASE_NAME)
        print(f"Database {DATABASE_NAME} berhasil direset!")

        # Mulai proses seeding data
        db = client[DATABASE_NAME]

        # Buat data admin pertama
        admin_data = {
            "email": "amangly@gmail.com",
            "username": "amangly",
            "full_name": "amangly palepale", 
            "password": get_password_hash("amangly123"),
            "is_admin": True,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        await db.users.insert_one(admin_data)
        print("Data admin berhasil dibuat!")

        # Buat data blog contoh
        blogs = [
            {
                "title": "Dampaknya Terhadap Stabilitas Global",
                "content": "Ketegangan di Laut China Selatan semakin meningkat seiring perebutan klaim wilayah dan sumber daya alam di kawasan tersebut. Konflik ini melibatkan berbagai negara besar seperti China, Filipina, Vietnam, dan Amerika Serikat...",
                "image": "/static/uploads/gallery1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Dampaknya Terhadap Stabilitas Global",
                "content": "Ketegangan di Laut China Selatan semakin meningkat seiring perebutan klaim wilayah dan sumber daya alam di kawasan tersebut. Konflik ini melibatkan berbagai negara besar seperti China, Filipina, Vietnam, dan Amerika Serikat...",
                "image": "/static/uploads/gallery2.jpg", 
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.blogs.insert_many(blogs)
        print(f"{len(blogs)} data blog berhasil dibuat!")

        # Buat data galeri contoh
        gallery = [
            {
                "title": "Foto Pertama",
                "description": "Deskripsi foto pertama",
                "image": "/static/uploads/gallery1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Foto Kedua",
                "description": "Deskripsi foto kedua", 
                "image": "/static/uploads/gallery2.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.gallery.insert_many(gallery)
        print("2 data galeri berhasil dibuat!")

        # Buat data partner contoh
        partners = [
            {
                "name": "Partner Pertama",
                "description": "Deskripsi partner pertama",
                "website_url": "https://partner1.com",
                "logo": "/static/uploads/partner1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "name": "Partner Kedua",
                "description": "Deskripsi partner kedua",
                "website_url": "https://partner2.com",
                "logo": "/static/uploads/partner2.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.partners.insert_many(partners)
        print("2 data partner berhasil dibuat!")

        # Buat data program contoh
        programs = [
            {
                "title": "Workshop Data Science",
                "subtitle": "Pengenalan Data Science untuk Pemula",
                "description": "Workshop pengenalan data science dengan materi dasar-dasar pengolahan data, visualisasi, dan machine learning",
                "image": "/static/uploads/program1.jpg",
                "created_at": datetime.utcnow()
            },
            {
                "title": "Seminar Artificial Intelligence",
                "subtitle": "Memahami Dampak AI dalam Kehidupan Sehari-hari",
                "description": "Seminar yang membahas tentang perkembangan AI dan dampaknya terhadap berbagai aspek kehidupan",
                "image": "/static/uploads/program2.jpg",
                "created_at": datetime.utcnow()
            },
            {
                "title": "Pelatihan Machine Learning",
                "subtitle": "Implementasi ML untuk Pemecahan Masalah",
                "description": "Pelatihan intensif tentang implementasi machine learning dalam menyelesaikan berbagai kasus nyata",
                "image": "/static/uploads/program3.jpg",
                "created_at": datetime.utcnow()
            }
        ]
        await db.programs.insert_many(programs)
        print("3 data program berhasil dibuat!")

        print("Proses seeding data selesai!")

    except Exception as e:
        print(f"Terjadi error saat seeding data: {str(e)}")
    finally:
        if client:
            client.close()
            print("Koneksi database telah ditutup.")

# Jalankan fungsi seeding jika file dijalankan langsung
if __name__ == "__main__":
    asyncio.run(seed_all())
```

Modul Seeder ini menyediakan fungsi-fungsi untuk:

1. Membuat user admin pertama
2. Mengisi data awal untuk blog
3. Mengisi data awal untuk gallery
4. Mengisi data awal untuk partners
5. Mengisi data awal untuk programs

Fitur utama:

- Pengecekan data existing sebelum seeding
- Password hashing untuk admin
- Konfigurasi dari environment variables
- Logging proses seeding
- Error handling untuk setiap operasi
- Koneksi database yang aman
- Data sample untuk testing

Cara Penggunaan:

1. Set environment variables untuk admin credentials
2. Jalankan script dengan `python -m app.utils.seeder`
3. Cek output untuk status seeding

Catatan:

- Seeder hanya berjalan jika data belum ada
- Password admin di-hash menggunakan bcrypt
- Semua data memiliki timestamp created_at
- Koneksi database ditutup setelah selesai

## TAHAP 5: TESTING API ENDPOINTS

### Langkah 1: Testing Authentication

1. Test Register endpoint dengan Postman:

```
POST /auth/register
Content-Type: application/json

{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
}
```

2. Test Login endpoint:

```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=password123
```

### Langkah 2: Testing Protected Endpoints

1. Setup Authorization:

   - Copy token dari response login
   - Di Postman, pilih tab "Authorization"
   - Type: Bearer Token
   - Paste token

2. Test Programs endpoints:

```
POST /programs
Content-Type: application/json

{
    "title": "Test Program",
    "description": "Test Description",
    "program_type": "workshop"
}
```

3. Test Blog dengan file upload:

```
POST /blogs
Content-Type: multipart/form-data

title: Test Blog
content: Test Content
image: [select file]
```

### Langkah 3: Error Testing

1. Test invalid authentication:

   - Use expired token
   - Use invalid token format
   - Try accessing protected routes without token

2. Test validation errors:

   - Submit invalid email format
   - Submit too short password
   - Submit invalid program_type

3. Test file upload errors:
   - Upload invalid file type
   - Upload too large file
   - Upload without required fields

## TAHAP 6: DOKUMENTASI API

### Langkah 1: Setup Swagger UI

1. Update main.py dengan metadata:

```python
app = FastAPI(
    title="Lembaga Sinergi Analitika API",
    description="API untuk mengelola program, blog, dan galeri",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "authentication",
            "description": "Operasi terkait autentikasi pengguna"
        },
        {
            "name": "programs",
            "description": "Operasi CRUD untuk program"
        },
        {
            "name": "blogs",
            "description": "Endpoint untuk manajemen blog"
        },
        {
            "name": "gallery",
            "description": "Endpoint untuk manajemen galeri"
        },
        {
            "name": "partners",
            "description": "Endpoint untuk manajemen partner"
        }
    ]
)
```

### Langkah 2: Dokumentasi Endpoints

1. Tambahkan docstrings ke setiap endpoint:

```python
@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister, db=Depends(get_database)):
    """
    Register new user with the following information:
    - email: valid email address
    - username: minimum 3 characters
    - password: minimum 6 characters
    """
```

## TAHAP 7: SECURITY ENHANCEMENTS

### Langkah 1: CORS Setup

1. Update main.py dengan CORS middleware:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sesuaikan dengan domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Langkah 2: Rate Limiting

1. Tambahkan rate limiting middleware:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### Langkah 3: Error Handling

1. Buat custom error handlers:

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

## TAHAP 8: DEPLOYMENT PREPARATION

### Langkah 1: Environment Setup

1. Buat file Dockerfile:

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Buat docker-compose.yml:

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - '8000:8000'
    depends_on:
      - mongodb
    environment:
      - MONGODB_URL=mongodb://mongodb:27017

  mongodb:
    image: mongo:latest
    ports:
      - '27017:27017'
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

### Langkah 2: Production Settings

1. Buat file .env.production:

```env
MONGODB_URL=mongodb://production-db:27017
DATABASE_NAME=lembaga_sinergi_analitika
SECRET_KEY=your-production-secret-key
DEBUG_MODE=False
```

2. Update security settings untuk production:

```python
# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update security headers
app.add_middleware(
    SecurityMiddleware,
    ssl_redirect=True,
    force_https=True,
)
```

### Langkah 3: Best Practices

1. Desain Payload

   - Jaga payload tetap kecil dan fokus
   - Sertakan hanya data yang diperlukan
   - Pertahankan struktur yang konsisten
   - Versikan payload webhook Anda

2. Penanganan Kesalahan

   - Terapkan mekanisme percobaan ulang
   - Catat pengiriman yang gagal
   - Pantau kesehatan webhook
   - Beri peringatan pada kegagalan berulang

3. Kinerja

   - Pemrosesan webhook secara asinkron
   - Kelompokkan event yang serupa
   - Terapkan pembatasan rate
   - Gunakan antrian webhook

4. Pemantauan
   - Lacak tingkat keberhasilan pengiriman
   - Pantau waktu respons
   - Beri peringatan pada tingkat kegagalan tinggi
   - Catat informasi kesalahan secara detail

## TAHAP 9: UNIT TESTING

### Langkah 1: Setup Testing Environment

1. Install dependencies untuk testing:

```bash
pip install pytest pytest-asyncio httpx pytest-cov
```

2. Buat file konfigurasi pytest.ini:

```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S
filterwarnings =
    ignore::DeprecationWarning
    ignore::UserWarning
```

### Langkah 2: Setup Test Fixtures (conftest.py)

1. Buat fixtures untuk database dan client testing:

```python
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
```

### Langkah 3: Implementasi Test Cases

1. Test Authentication (test_auth.py):

```python
@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient, db_client):
    """Test registrasi berhasil"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status_code == 201
```

2. Test Blog (test_blog.py):

```python
@pytest.mark.asyncio
async def test_create_blog(async_client: AsyncClient):
    """Test membuat blog baru"""
    # Login untuk mendapatkan token
    response = await async_client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]

    # Buat blog dengan gambar
    files = {
        "image": ("test.jpg", image_content, "image/jpeg"),
        "title": (None, "Test Blog"),
        "content": (None, "Test content")
    }
    response = await async_client.post("/blogs", files=files, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

3. Test Gallery (test_gallery.py):

```python
@pytest.mark.asyncio
async def test_create_gallery(async_client: AsyncClient):
    """Test menambahkan foto ke galeri"""
    # Setup dan login
    files = {
        "image": ("test.jpg", image_content, "image/jpeg"),
        "title": (None, "Test Gallery"),
        "description": (None, "Test description")
    }
    response = await async_client.post("/gallery", files=files, headers=headers)
    assert response.status_code == 200
```

4. Test Partners (test_partners.py):

```python
@pytest.mark.asyncio
async def test_create_partner(async_client: AsyncClient):
    """Test menambahkan partner baru"""
    files = {
        "logo": ("test.jpg", logo_content, "image/jpeg"),
        "name": (None, "Test Partner"),
        "description": (None, "Test description"),
        "website_url": (None, "https://www.example.com/")
    }
    response = await async_client.post("/partners", files=files, headers=headers)
    assert response.status_code == 200
```

5. Test Programs (test_programs.py):

```python
@pytest.mark.asyncio
async def test_create_program(async_client: AsyncClient):
    """Test membuat program baru"""
    files = {
        "image": ("test.jpg", image_content, "image/jpeg"),
        "title": (None, "Test Program"),
        "description": (None, "Test description"),
        "program_type": (None, "workshop"),
        "start_date": (None, start_date.isoformat()),
        "end_date": (None, end_date.isoformat())
    }
    response = await async_client.post("/programs", files=files, headers=headers)
    assert response.status_code == 200
```

### Langkah 4: Menjalankan Tests

1. Jalankan semua test:

```bash
pytest app/tests/ -v
```

2. Jalankan test spesifik:

```bash
pytest app/tests/test_auth.py -v
```

3. Jalankan test dengan coverage:

```bash
pytest --cov=app app/tests/
```

### Fitur Testing yang Diimplementasikan:

1. **Database Testing**:

   - Menggunakan database terpisah untuk testing
   - Membersihkan database sebelum dan sesudah setiap test
   - Penanganan koneksi database yang aman

2. **Authentication Testing**:

   - Test registrasi user
   - Test login dengan kredensial valid
   - Test login dengan kredensial invalid
   - Test duplikasi email dan username

3. **CRUD Testing**:

   - Create: Test pembuatan data baru
   - Read: Test pengambilan data
   - Delete: Test penghapusan data
   - Validasi response status dan content

4. **File Upload Testing**:

   - Test upload gambar
   - Validasi format file
   - Penanganan file storage

5. **Error Handling**:

   - Test case untuk error cases
   - Validasi pesan error
   - Penanganan exception

6. **Security Testing**:
   - Test autentikasi token
   - Test akses unauthorized
   - Validasi permission
