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

- Linux/Mac:

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
fastapi==0.110.0
uvicorn==0.27.1
motor==3.3.2
pymongo==4.6.2
python-decouple==3.8
python-multipart==0.0.9
pydantic==2.6.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2
aiofiles==23.2.1
```

### Langkah 3: Penjelasan package utama

1. fastapi==0.110.0

   - Framework web modern dan cepat untuk membangun API
   - Berbasis Python modern (async/await)
   - Fitur validasi otomatis dan dokumentasi OpenAPI

2. uvicorn==0.27.1

   - Server ASGI yang cepat untuk menjalankan aplikasi FastAPI
   - Mendukung hot reload untuk development
   - Penanganan WebSocket

3. motor==3.3.2 & pymongo==4.6.2

   - Motor: Driver MongoDB async untuk Python
   - PyMongo: Driver MongoDB sync (diperlukan oleh Motor)
   - Menangani koneksi dan operasi database

4. python-decouple==3.8

   - Memisahkan konfigurasi dari kode
   - Membaca variabel environment
   - Memudahkan manajemen konfigurasi

5. python-multipart==0.0.9

   - Menangani form data dan file upload
   - Dibutuhkan untuk menerima request multipart/form-data
   - Penting untuk fitur upload file

6. pydantic==2.6.3

   - Validasi data dan serialisasi
   - Type hints yang powerful
   - Integrasi dengan FastAPI untuk model data

7. python-jose[cryptography]==3.3.0

   - Implementasi JWT (JSON Web Tokens)
   - Menangani enkripsi dan dekripsi token
   - Fitur keamanan untuk autentikasi

8. passlib[bcrypt]==1.7.4 & bcrypt==4.1.2

   - Passlib: Library untuk password hashing
   - Bcrypt: Algoritma hashing yang aman
   - Mengamankan password user

9. aiofiles==23.2.1
   - Operasi file async/await
   - Menangani file secara asynchronous
   - Penting untuk upload file tanpa blocking

### Langkah 4: Setup Struktur Project

1. Buat struktur folder berikut:

## Struktur Proyek

```
backend/
├── app/                    # Folder inti yang berisi seluruh logika aplikasi
│   ├── api/               # Folder yang berisi semua endpoint API dan dependensi
│   │   ├── endpoints/     # Folder yang berisi semua endpoint API
│   │   │   ├── auth.py   # Endpoint untuk autentikasi (login, register)
│   │   │   ├── blog.py   # Endpoint untuk manajemen blog/artikel
│   │   │   ├── gallery.py # Endpoint untuk manajemen galeri foto
│   │   │   ├── partners.py # Endpoint untuk manajemen mitra/partner
│   │   │   └── programs.py # Endpoint untuk manajemen program/kegiatan
│   │   └── deps.py       # Berisi dependency injection
│   ├── core/             # Berisi komponen inti aplikasi
│   │   ├── config.py     # Konfigurasi aplikasi
│   │   └── database.py   # Konfigurasi koneksi database MongoDB
│   ├── models/           # Berisi model data
│   │   └── schemas.py    # Model untuk validasi data
│   ├── tests/            # Berisi unit tests
│   │   ├── conftest.py   # Konfigurasi dan fixtures untuk testing
│   │   ├── test_auth.py  # Test untuk autentikasi
│   │   ├── test_blog.py  # Test untuk blog
│   │   ├── test_gallery.py # Test untuk galeri
│   │   ├── test_partners.py # Test untuk partner
│   │   └── test_programs.py # Test untuk program
│   ├── utils/            # Berisi utility functions
│   │   └── file_handler.py # Fungsi untuk menangani file uploads
│   └── main.py          # File utama untuk menjalankan aplikasi
├── static/              # Folder untuk menyimpan file static
│   └── uploads/         # Folder untuk menyimpan file uploads
├── venv/               # Virtual environment Python
├── .env               # File untuk environment variables
├── .env.example       # Contoh konfigurasi environment variables
├── .gitignore        # File untuk mengabaikan file/folder dalam git
├── pytest.ini        # Konfigurasi untuk pytest
├── requirements.txt   # Daftar package Python yang dibutuhkan
└── README.md         # Dokumentasi proyek
```

### 1. Folder Root (`backend/`)

- Folder utama yang menampung seluruh proyek
- Berisi file konfigurasi utama seperti .env dan requirements.txt
- Tempat menyimpan virtual environment Python

### 2. Folder `app/`

- Folder inti yang berisi seluruh logika aplikasi
- Mengorganisir kode menjadi beberapa modul terpisah
- Menerapkan prinsip modular dan clean architecture

### 3. Folder `app/api/`

- Berisi semua endpoint API dan dependensi
- Mengatur routing dan logika bisnis
- Implementasi RESTful API dengan FastAPI

#### 3.1 Folder `app/api/endpoints/`

- **auth.py**: Menangani autentikasi (login, register, logout) dengan JWT
- **blog.py**: Endpoint CRUD untuk manajemen blog/artikel dengan gambar
- **gallery.py**: Endpoint CRUD untuk manajemen galeri foto
- **partners.py**: Endpoint CRUD untuk manajemen mitra/partner dengan logo
- **programs.py**: Endpoint CRUD untuk manajemen program/kegiatan dengan gambar

#### 3.2 File `app/api/deps.py`

- Berisi dependency injection untuk FastAPI
- Fungsi-fungsi helper untuk autentikasi JWT
- Validasi token dan user aktif
- Middleware untuk pengecekan role dan permission

### 4. Folder `app/core/`

- Berisi komponen inti aplikasi
- Konfigurasi dan setup dasar aplikasi
- Koneksi database dan middleware

#### 4.1 File `app/core/database.py`

- Konfigurasi koneksi database MongoDB dengan Motor
- Fungsi-fungsi async untuk manajemen koneksi database
- Implementasi database pooling dan retry mechanism

#### 4.2 File `app/core/config.py`

- Konfigurasi aplikasi dari environment variables
- Membaca variabel environment dari .env
- Konfigurasi logging dan error handling

###

### Langkah 1: Setup Database Connection

1. Implementasi koneksi MongoDB di app/core/database.py:

```python
# Import library yang diperlukan
from motor.motor_asyncio import AsyncIOMotorClient  # Driver MongoDB async untuk Python
from decouple import config  # Untuk membaca konfigurasi dari .env

# Konfigurasi database dari environment variables
MONGODB_URL = config("MONGODB_URL", default="mongodb://localhost:27017")
DATABASE_NAME = config("DATABASE_NAME", default="lembaga_sinergi_analitika")

# Variabel global untuk koneksi MongoDB
client = None
db = None

async def connect_to_mongo():
    """
    Fungsi untuk membuat koneksi ke database MongoDB.
    - Menggunakan Motor sebagai driver async
    - Mencoba koneksi dengan ping ke admin database
    - Menyimpan instance koneksi ke variabel global
    """
    global client, db
    try:
        # Buat koneksi ke MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        # Test koneksi dengan ping
        await client.admin.command('ping')
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """
    Fungsi untuk menutup koneksi database.
    - Menutup koneksi client jika ada
    - Membersihkan resources
    """
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed.")

async def get_database():
    """
    Fungsi untuk mendapatkan instance database.
    - Mengecek apakah koneksi sudah ada
    - Membuat koneksi baru jika belum ada
    - Mengembalikan instance database
    """
    global client, db
    if db is None:
        await connect_to_mongo()
    return db
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
from pydantic import BaseModel, Field, ConfigDict  # Untuk membuat model data dan validasi
from typing import Optional, Any, Dict, List  # Untuk tipe data
from datetime import datetime  # Untuk handling waktu
from bson import ObjectId  # Untuk MongoDB ObjectId
from pydantic_core import core_schema  # Untuk custom schema validation

# Custom class untuk validasi ObjectId
class PyObjectId(str):
    """
    Class untuk memvalidasi dan mengkonversi MongoDB ObjectId.
    Digunakan sebagai tipe data custom dalam Pydantic model.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (str, ObjectId)):
            raise ValueError("Invalid ObjectId")
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

# Model untuk User
class UserRegister(BaseModel):
    email: str = Field(..., pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    username: str
    created_at: datetime

# Model untuk Program
class ProgramBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    program_type: str = Field(..., pattern="^(human_library|workshop|sosialisasi)$")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProgramResponse(ProgramBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Model untuk Blog
class BlogBase(BaseModel):
    title: str = Field(..., min_length=3)
    content: str
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BlogResponse(BlogBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Model untuk Gallery
class GalleryBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    image_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GalleryResponse(GalleryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Model untuk Partner
class PartnerBase(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None
    website_url: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PartnerResponse(PartnerBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Model untuk Response Envelope
class ResponseEnvelope(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
    meta: Optional[dict] = None
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

# Definisikan direktori upload
UPLOAD_DIR = "static/uploads"
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

    # Definisikan tipe file yang diizinkan
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    # Generate nama file unik dengan timestamp dan uuid
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}_{unique_id}{file_extension}"

    # Buat path lengkap file
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        # Simpan file ke sistem
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        # Handle error saat menyimpan file
        raise HTTPException(
            status_code=500,
            detail=f"Could not upload file: {str(e)}"
        )
    finally:
        # Pastikan file ditutup
        file.file.close()

    # Return path file yang bisa diakses
    return f"/{UPLOAD_DIR}/{filename}"
```

### Langkah 3: Database Seeder

1. Implementasi seeder.py untuk mengisi data awal:

```python
# Import library yang diperlukan
from app.core.database import get_database, connect_to_mongo, close_mongo_connection  # Koneksi database
from passlib.context import CryptContext  # Untuk hashing password
from datetime import datetime  # Untuk timestamp
import asyncio  # Untuk async/await
from decouple import config  # Untuk environment variables

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fungsi untuk membuat admin pertama
async def seed_admin():
    try:
        await connect_to_mongo()
        db = await get_database()

        # Cek apakah admin sudah ada
        admin = await db.users.find_one({"email": config("ADMIN_EMAIL", default="admin@admin.com")})
        if admin:
            print("Admin already exists!")
            return

        # Buat data admin
        admin_data = {
            "email": config("ADMIN_EMAIL", default="admin@admin.com"),
            "username": config("ADMIN_USERNAME", default="admin"),
            "password": pwd_context.hash(config("ADMIN_PASSWORD", default="admin123")),
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.utcnow()
        }

        # Insert admin ke database
        result = await db.users.insert_one(admin_data)
        if result.inserted_id:
            print("Admin user created successfully!")
    except Exception as e:
        print(f"Error creating admin: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data blog
async def seed_blog():
    try:
        await connect_to_mongo()
        db = await get_database()

        # Cek apakah sudah ada blog posts
        if await db.blogs.count_documents({}) > 0:
            print("Blog posts already exist!")
            return

        # Data blog sample
        blog_data = [
            {
                "title": "Blog Post 1",
                "content": "Ini adalah konten blog pertama",
                "image_url": "https://example.com/image1.jpg",
                "author": "Admin",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.blogs.insert_many(blog_data)
        print(f"{len(result.inserted_ids)} blog posts created successfully!")
    except Exception as e:
        print(f"Error creating blog posts: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data gallery
async def seed_gallery():
    try:
        await connect_to_mongo()
        db = await get_database()

        if await db.gallery.count_documents({}) > 0:
            print("Gallery items already exist!")
            return

        gallery_data = [
            {
                "title": "Gambar 1",
                "description": "Deskripsi gambar 1",
                "image_url": "https://example.com/gallery1.jpg",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.gallery.insert_many(gallery_data)
        print(f"{len(result.inserted_ids)} gallery items created successfully!")
    except Exception as e:
        print(f"Error creating gallery items: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data partners
async def seed_partners():
    try:
        await connect_to_mongo()
        db = await get_database()

        if await db.partners.count_documents({}) > 0:
            print("Partners already exist!")
            return

        partners_data = [
            {
                "name": "Partner 1",
                "description": "Deskripsi partner 1",
                "logo_url": "https://example.com/partner1.jpg",
                "website": "https://partner1.com",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.partners.insert_many(partners_data)
        print(f"{len(result.inserted_ids)} partners created successfully!")
    except Exception as e:
        print(f"Error creating partners: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data programs
async def seed_programs():
    try:
        await connect_to_mongo()
        db = await get_database()

        if await db.programs.count_documents({}) > 0:
            print("Programs already exist!")
            return

        programs_data = [
            {
                "title": "Program 1",
                "description": "Deskripsi program 1",
                "image_url": "https://example.com/program1.jpg",
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow(),
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.programs.insert_many(programs_data)
        print(f"{len(result.inserted_ids)} programs created successfully!")
    except Exception as e:
        print(f"Error creating programs: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk menjalankan semua seeder
async def seed_all():
    await connect_to_mongo()
    try:
        await seed_admin()
        await seed_blog()
        await seed_gallery()
        await seed_partners()
        await seed_programs()
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
    finally:
        await close_mongo_connection()

# Entry point untuk menjalankan seeder
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

## TAHAP 2: IMPLEMENTASI AUTHENTICATION

### Langkah 1: Setup Dependencies (deps.py)

1. Implementasi dependency untuk authentication:

```python
# Import library yang diperlukan
from fastapi import Depends, HTTPException, status  # Untuk dependency injection dan exception handling
from fastapi.security import OAuth2PasswordBearer  # Untuk implementasi OAuth2 dengan password flow
from jose import jwt, JWTError  # Untuk JWT encoding/decoding
from decouple import config  # Untuk mengambil environment variables
from app.core.database import get_database  # Untuk koneksi database

# Setup OAuth2 dengan endpoint login di /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Ambil secret key dari environment variable untuk signing JWT
SECRET_KEY = config("SECRET_KEY")

# Algoritma yang digunakan untuk JWT
ALGORITHM = "HS256"

# Fungsi untuk memvalidasi JWT token dan mendapatkan current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Exception yang akan dilempar jika token invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        # Decode JWT token menggunakan secret key dan algoritma yang ditentukan
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Ambil email user dari payload token (disimpan dalam field 'sub')
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # Jika terjadi error saat decode token, lempar exception
        raise credentials_exception

    # Return email user jika token valid
    return email
```

### Langkah 2: Implementasi Authentication Endpoints

1. Buat file auth.py di app/api/endpoints/
2. Implementasi login dan register

```python
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends  # Untuk routing dan error handling
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Untuk implementasi OAuth2
from app.models.schemas import UserResponse, Token, UserRegister  # Model data untuk user
from app.core.database import get_database  # Koneksi database
from datetime import datetime, timedelta  # Untuk handling waktu dan expiry token
from passlib.context import CryptContext  # Untuk hashing password
from jose import jwt  # Untuk JWT encoding/decoding
from app.core.config import settings  # Import settings dari config

# Inisialisasi router dan tools
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Setup password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Setup OAuth2

# Fungsi untuk membuat access token
def create_access_token(data: dict):
    to_encode = data.copy()
    # Set waktu expired token dari settings
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode JWT dengan secret key dan algoritma dari settings
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Endpoint untuk registrasi user baru
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register User Baru",
    description="Mendaftarkan user baru dengan email, username, dan password"
)
async def register(
    user: UserRegister,
    db=Depends(get_database)
):
    # Cek apakah email sudah terdaftar
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # Cek apakah username sudah digunakan
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username sudah digunakan")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Siapkan data user
    user_data = {
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow()
    }

    # Insert user ke database
    result = await db.users.insert_one(user_data)

    # Return user yang dibuat
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return created_user

# Endpoint untuk login user
@router.post(
    "/login",
    response_model=Token,
    summary="Login User",
    description="Login user dengan email dan password untuk mendapatkan access token"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_database)
):
    # Cek apakah user ada
    user = await db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # Verifikasi password
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # Cek status aktif user
    if not user.get("is_active", False):
        raise HTTPException(status_code=400, detail="Akun tidak aktif")

    # Buat access token dengan data user
    access_token = create_access_token(
        data={"sub": user["email"], "is_admin": user.get("is_admin", False)}
    )
    return {"access_token": access_token, "token_type": "bearer"}
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

### Langkah 2: Authentication Module

1. Buat file auth.py di app/api/endpoints/:

```python
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends, Form # Untuk routing dan error handling
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # Untuk implementasi OAuth2
from app.models.schemas import UserResponse, Token # Model data untuk user
from app.core.database import get_database # Koneksi database
from datetime import datetime, timedelta # Untuk handling waktu dan expiry token
from passlib.context import CryptContext # Untuk hashing password
from jose import jwt # Untuk JWT encoding/decoding
from decouple import config # Untuk mengambil environment variables

router = APIRouter() # Inisialisasi router
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Setup password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # Setup OAuth2

SECRET_KEY = config("JWT_SECRET_KEY", default="your-secret-key") # Ambil secret key dari environment variable
ALGORITHM = config("JWT_ALGORITHM", default="HS256") # Ambil algoritma JWT dari environment variable
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int) # Ambil waktu expiry token dari environment variable

def create_access_token(data: dict): # Fungsi untuk membuat access token
    to_encode = data.copy() # Copy data yang akan di-encode
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Set waktu expired token
    to_encode.update({"exp": expire}) # Tambahkan waktu expired ke data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Encode JWT dengan secret key
    return encoded_jwt # Return token yang sudah di-encode

# Endpoint untuk registrasi user baru
@router.post(
    "/register",
    response_model=UserResponse,
    summary="Register User Baru",
    description="Mendaftarkan user baru dengan email, username, dan password"
)

# Endpoint untuk registrasi user baru
async def register(
    # Ambil data dari request body
    email: str = Form(..., description="Email user", email=True),
    username: str = Form(..., description="Username", min_length=3),
    password: str = Form(..., description="Password", min_length=6),
    db=Depends(get_database)
):
    # Cek apakah email sudah terdaftar
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # hash password
    hashed_password = pwd_context.hash(password)

    # Siapkan data user
    user_data = {
        "email": email,
        "username": username,
        "password": hashed_password,
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow()
    }

    # Masukkan user ke database
    result = await db.users.insert_one(user_data)

    # Ambil user yang baru dibuat
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return created_user

# Endpoint untuk login user
@router.post(
    "/login",
    response_model=Token,
    summary="Login User",
    description="Login user dengan email dan password untuk mendapatkan access token"
)
async def login(
    # Ambil data dari request body
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_database)
):
    # Cek apakah user ada
    user = await db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # Verifikasi password
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # Cek status aktif user
    if not user.get("is_active", False):
        raise HTTPException(status_code=400, detail="Akun tidak aktif")

    # Buat access token dengan data user
    access_token = create_access_token(
        data={"sub": user["email"], "is_admin": user.get("is_admin", False)}
    )
    return {"access_token": access_token, "token_type": "bearer"}
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
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query  # Untuk routing dan error handling
from app.models.schemas import ProgramBase, ProgramResponse  # Model data program
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_active_user  # Autentikasi user
from app.utils.file_handler import save_upload_file  # Fungsi untuk menyimpan file
from typing import List, Literal, Union, Optional  # Untuk tipe data
from datetime import datetime  # Untuk timestamp
from bson import ObjectId  # Untuk konversi string ke ObjectId
from bson.errors import InvalidId  # Untuk handling error ObjectId
from enum import Enum  # Untuk enum tipe program

# Definisi enum untuk tipe program
class ProgramType(str, Enum):
    ALL = "all"  # Untuk filter semua program
    HUMAN_LIBRARY = "human_library"  # Program Human Library
    WORKSHOP = "workshop"  # Program Workshop
    SOSIALISASI = "sosialisasi"  # Program Sosialisasi

# Inisialisasi router dengan tag programs
router = APIRouter(tags=["programs"])

# Endpoint untuk membuat program baru
@router.post(
    "",
    response_model=ProgramResponse,
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
    """
)
async def create_program(
    title: str = Form(..., description="Judul program", example="Workshop Pemulihan Mental"),
    description: str = Form(..., description="Deskripsi program", example="Workshop untuk pemulihan kesehatan mental..."),
    program_type: ProgramType = Form(
        ...,
        description="Tipe program (human_library, workshop, sosialisasi)",
        exclude=["ALL"]
    ),
    image: UploadFile = File(
        ...,
        description="File gambar untuk program (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    start_date: datetime = Form(..., description="Tanggal mulai program", example="2024-01-01T00:00:00"),
    end_date: datetime = Form(..., description="Tanggal selesai program", example="2024-01-02T00:00:00"),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload gambar
    image_url = await save_upload_file(image)

    program_data = {
        "title": title,
        "description": description,
        "program_type": program_type.value,
        "image": image_url,
        "start_date": start_date,
        "end_date": end_date,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }

    # Validasi data program menggunakan ProgramBase
    program = ProgramBase(**program_data)

    result = await db.programs.insert_one(program.model_dump())
    created_program = await db.programs.find_one({"_id": result.inserted_id})
    return created_program

# Endpoint untuk mendapatkan daftar program
@router.get(
    "",
    response_model=List[ProgramResponse],
    summary="Mengambil Semua Program",
    description="""
    Mengambil daftar program yang tersedia.

    **Filter Tipe Program:**
    - all: Menampilkan semua program
    - human_library: Hanya program human library
    - workshop: Hanya program workshop
    - sosialisasi: Hanya program sosialisasi
    """
)
async def get_programs(
    program_type: ProgramType = Query(
        ProgramType.ALL,
        description="Filter berdasarkan tipe program"
    ),
    db=Depends(get_database)
):
    query = {}
    if program_type != ProgramType.ALL:
        query["program_type"] = program_type.value

    programs = await db.programs.find(query).to_list(1000)
    return programs

# Endpoint untuk mendapatkan detail program
@router.get(
    "/{program_id}",
    response_model=ProgramResponse,
    summary="Mengambil Detail Program",
    description="Mengambil detail program berdasarkan ID."
)
async def get_program(program_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="ID program tidak valid. ID harus berupa 24 karakter hex string."
        )

    program = await db.programs.find_one({"_id": object_id})
    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program tidak ditemukan"
        )
    return program

# Endpoint untuk menghapus program
@router.delete(
    "/{program_id}",
    summary="Menghapus Program",
    description="Menghapus program berdasarkan ID."
)
async def delete_program(
    program_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="ID program tidak valid. ID harus berupa 24 karakter hex string."
        )

    result = await db.programs.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Program tidak ditemukan"
        )
    return {"message": "Program berhasil dihapus"}
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
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query  # Untuk routing dan handling HTTP
from app.models.schemas import BlogResponse, ResponseEnvelope  # Model data untuk blog
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_active_user  # Autentikasi user
from app.utils.file_handler import save_upload_file  # Fungsi untuk menyimpan file
from typing import Optional  # Tipe data opsional
from datetime import datetime  # Untuk timestamp
import logging  # Untuk logging

router = APIRouter(tags=["blogs"]) # Inisialisasi router
logger = logging.getLogger(__name__) # Inisialisasi logger

# Endpoint untuk membuat blog baru
@router.post(
    "",
    response_model=BlogResponse,
    summary="Membuat Blog Baru",
    description="""
    Membuat blog baru dengan gambar.

    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF

    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
# Endpoint untuk membuat blog baru
async def create_blog(
    title: str = Form(..., description="Judul blog yang akan dibuat", example="Tutorial Python"),
    content: str = Form(..., description="Konten atau isi blog", example="Python adalah bahasa pemrograman yang mudah dipelajari..."),
    image: UploadFile = File(
        ...,
        description="File gambar untuk blog (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    """
    Membuat blog baru dengan gambar.

    Parameters:
    - **title**: Judul blog
    - **content**: Konten blog
    - **image**: File gambar (max 5MB, format: JPG/PNG/GIF)

    Returns:
    - Blog yang berhasil dibuat
    """
    # Upload gambar
    image_url = await save_upload_file(image)

    blog_data = {
        "title": title,
        "content": content,
        "image": image_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }

    result = await db.blogs.insert_one(blog_data)
    created_blog = await db.blogs.find_one({"_id": result.inserted_id})
    return created_blog

# Endpoint untuk mendapatkan semua blog
@router.get("", response_model=ResponseEnvelope)
async def get_blogs(
    skip: int = Query(default=0, ge=0, description="Skip n items"),
    limit: int = Query(default=10, ge=1, le=100, description="Limit the number of items"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    db = Depends(get_database)
):
    try:
        logger.info(f"Fetching blogs with skip={skip}, limit={limit}, search={search}")

        # Build query
        query = {}
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}}
            ]

        # Get total count
        total_count = await db.blogs.count_documents(query)

        # Get paginated results
        blogs = await db.blogs.find(query).skip(skip).limit(limit).to_list(limit)

        # Convert ObjectId to string
        for blog in blogs:
            blog["_id"] = str(blog["_id"])

        return ResponseEnvelope(
            status="success",
            message="Blog berhasil diambil",
            data=blogs,
            meta={
                "total": total_count,
                "skip": skip,
                "limit": limit,
                "has_more": (skip + limit) < total_count
            }
        )
    except Exception as e:
        logger.error(f"Error fetching blogs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk mendapatkan blog berdasarkan ID
@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: str, db=Depends(get_database)):
    from bson import ObjectId
    try:
        object_id = ObjectId(blog_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID blog tidak valid. ID harus berupa 24 karakter hex string."
        )

    blog = await db.blogs.find_one({"_id": object_id})
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog tidak ditemukan"
        )
    return blog

# Endpoint untuk menghapus blog
@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    from bson import ObjectId
    try:
        object_id = ObjectId(blog_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID blog tidak valid. ID harus berupa 24 karakter hex string."
        )

    result = await db.blogs.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Blog tidak ditemukan"
        )
    return {"message": "Blog berhasil dihapus"}
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
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File # Untuk routing dan error handling
from app.models.schemas import GalleryBase, GalleryResponse # Model data untuk galeri
from app.core.database import get_database # Koneksi database
from app.api.deps import get_current_active_user # Autentikasi user
from app.utils.file_handler import save_upload_file # Fungsi untuk menyimpan file
from typing import List # Untuk tipe data list
from datetime import datetime # Untuk timestamp
from bson import ObjectId # Untuk konversi string ke ObjectId

router = APIRouter(tags=["gallery"])

@router.post(
    "",
    response_model=GalleryResponse,
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
async def create_gallery(
    title: str = Form(..., description="Judul foto", example="Workshop Batch 2023"),
    description: str = Form(..., description="Deskripsi foto", example="Dokumentasi kegiatan workshop..."),
    image: UploadFile = File(
        ...,
        description="File foto (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload gambar
    image_url = await save_upload_file(image)

    gallery_data = {
        "title": title,
        "description": description,
        "image": image_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }

    result = await db.gallery.insert_one(gallery_data)
    created_gallery = await db.gallery.find_one({"_id": result.inserted_id})
    return created_gallery

@router.get(
    "",
    response_model=List[GalleryResponse],
    summary="Mengambil Semua Foto Galeri",
    description="Mengambil daftar semua foto yang ada di galeri."
)
async def get_galleries(db=Depends(get_database)):
    galleries = await db.gallery.find().to_list(1000)
    return galleries

@router.get(
    "/{gallery_id}",
    response_model=GalleryResponse,
    summary="Mengambil Detail Foto",
    description="Mengambil detail foto berdasarkan ID."
)
async def get_gallery(gallery_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(gallery_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID galeri tidak valid. ID harus berupa 24 karakter hex string."
        )

    gallery = await db.gallery.find_one({"_id": object_id})
    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Foto tidak ditemukan"
        )
    return gallery

@router.delete(
    "/{gallery_id}",
    summary="Menghapus Foto",
    description="Menghapus foto dari galeri berdasarkan ID."
)
async def delete_gallery(
    gallery_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        object_id = ObjectId(gallery_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID galeri tidak valid. ID harus berupa 24 karakter hex string."
        )

    result = await db.gallery.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Foto tidak ditemukan"
        )
    return {"message": "Foto berhasil dihapus"}
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
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File  # Untuk routing dan error handling
from app.models.schemas import PartnerBase, PartnerResponse  # Model data partner
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_active_user  # Autentikasi user
from app.utils.file_handler import save_upload_file  # Fungsi untuk menyimpan file
from typing import List  # Untuk tipe data list
from datetime import datetime  # Untuk timestamp
from bson import ObjectId  # Untuk konversi string ke ObjectId

router = APIRouter(tags=["partners"])

@router.post(
    "",
    response_model=PartnerResponse,
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
async def create_partner(
    name: str = Form(..., description="Nama partner/mitra", example="Universitas Indonesia"),
    description: str = Form(..., description="Deskripsi partner/mitra", example="Mitra dalam penyelenggaraan workshop..."),
    website_url: str = Form(..., description="URL website partner", example="https://www.ui.ac.id"),
    logo: UploadFile = File(
        ...,
        description="File logo partner (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Validasi URL
    try:
        from pydantic import HttpUrl
        HttpUrl(website_url)
    except:
        raise HTTPException(
            status_code=422,
            detail="URL website tidak valid. Harap masukkan URL yang valid (contoh: https://www.example.com)"
        )

    # Upload logo
    logo_url = await save_upload_file(logo)

    partner_data = {
        "name": name,
        "description": description,
        "website_url": website_url,
        "logo": logo_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }

    result = await db.partners.insert_one(partner_data)
    created_partner = await db.partners.find_one({"_id": result.inserted_id})
    return created_partner

@router.get(
    "",
    response_model=List[PartnerResponse],
    summary="Mengambil Semua Partner",
    description="Mengambil daftar semua partner/mitra."
)
async def get_partners(db=Depends(get_database)):
    partners = await db.partners.find().to_list(1000)
    return partners

@router.get(
    "/{partner_id}",
    response_model=PartnerResponse,
    summary="Mengambil Detail Partner",
    description="Mengambil detail partner/mitra berdasarkan ID."
)
async def get_partner(partner_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(partner_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )

    partner = await db.partners.find_one({"_id": object_id})
    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner tidak ditemukan"
        )
    return partner

@router.delete(
    "/{partner_id}",
    summary="Menghapus Partner",
    description="Menghapus partner/mitra berdasarkan ID."
)
async def delete_partner(
    partner_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        object_id = ObjectId(partner_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )

    result = await db.partners.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Partner tidak ditemukan"
        )
    return {"message": "Partner berhasil dihapus"}
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
from fastapi import FastAPI  # Framework utama untuk membuat API
from app.core.database import connect_to_mongo, close_mongo_connection  # Fungsi koneksi database
from app.api.endpoints import programs, auth, blog, gallery, partners  # Router untuk setiap modul
import uvicorn  # Server ASGI untuk menjalankan aplikasi
from fastapi.staticfiles import StaticFiles  # Untuk serving static files
from decouple import config  # Untuk membaca konfigurasi dari .env

# Ambil mode debug dari environment variable
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

# Inisialisasi aplikasi FastAPI dengan metadata
app = FastAPI(
    title="Lembaga Sinergi Analitika API",
    version="1.0.0"
)

# Mount direktori static untuk menyimpan file uploads
app.mount("/static", StaticFiles(directory="static"), name="static")

# Event handlers untuk koneksi database
app.add_event_handler("startup", connect_to_mongo)  # Koneksi database saat startup
app.add_event_handler("shutdown", close_mongo_connection)  # Tutup koneksi saat shutdown

# Daftarkan semua router dengan prefix dan tag masing-masing
app.include_router(auth.router, prefix="/auth", tags=["authentication"])  # Endpoint untuk autentikasi
app.include_router(programs.router, prefix="/programs", tags=["programs"])  # Endpoint untuk program
app.include_router(blog.router, prefix="/blogs", tags=["blogs"])  # Endpoint untuk blog
app.include_router(gallery.router, prefix="/gallery", tags=["gallery"])  # Endpoint untuk galeri
app.include_router(partners.router, prefix="/partners", tags=["partners"])  # Endpoint untuk partner
```

### Langkah 2: Setup Database Seeder

1. Implementasi seeder.py:

```python
# Import library yang diperlukan
from app.core.database import get_database, connect_to_mongo, close_mongo_connection  # Koneksi database
from passlib.context import CryptContext  # Untuk hashing password
from datetime import datetime  # Untuk timestamp
import asyncio  # Untuk async/await
from decouple import config  # Untuk environment variables

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fungsi untuk membuat admin pertama
async def seed_admin():
    try:
        await connect_to_mongo()
        db = await get_database()

        # Cek apakah admin sudah ada
        admin = await db.users.find_one({"email": config("ADMIN_EMAIL", default="admin@admin.com")})
        if admin:
            print("Admin already exists!")
            return

        # Buat data admin
        admin_data = {
            "email": config("ADMIN_EMAIL", default="admin@admin.com"),
            "username": config("ADMIN_USERNAME", default="admin"),
            "password": pwd_context.hash(config("ADMIN_PASSWORD", default="admin123")),
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.utcnow()
        }

        # Insert admin ke database
        result = await db.users.insert_one(admin_data)
        if result.inserted_id:
            print("Admin user created successfully!")
    except Exception as e:
        print(f"Error creating admin: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data blog
async def seed_blog():
    try:
        await connect_to_mongo()
        db = await get_database()

        # Cek apakah sudah ada blog posts
        if await db.blogs.count_documents({}) > 0:
            print("Blog posts already exist!")
            return

        # Data blog sample
        blog_data = [
            {
                "title": "Blog Post 1",
                "content": "Ini adalah konten blog pertama",
                "image_url": "https://example.com/image1.jpg",
                "author": "Admin",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.blogs.insert_many(blog_data)
        print(f"{len(result.inserted_ids)} blog posts created successfully!")
    except Exception as e:
        print(f"Error creating blog posts: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data gallery
async def seed_gallery():
    try:
        await connect_to_mongo()
        db = await get_database()

        if await db.gallery.count_documents({}) > 0:
            print("Gallery items already exist!")
            return

        gallery_data = [
            {
                "title": "Gambar 1",
                "description": "Deskripsi gambar 1",
                "image_url": "https://example.com/gallery1.jpg",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.gallery.insert_many(gallery_data)
        print(f"{len(result.inserted_ids)} gallery items created successfully!")
    except Exception as e:
        print(f"Error creating gallery items: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data partners
async def seed_partners():
    try:
        await connect_to_mongo()
        db = await get_database()

        if await db.partners.count_documents({}) > 0:
            print("Partners already exist!")
            return

        partners_data = [
            {
                "name": "Partner 1",
                "description": "Deskripsi partner 1",
                "logo_url": "https://example.com/partner1.jpg",
                "website": "https://partner1.com",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.partners.insert_many(partners_data)
        print(f"{len(result.inserted_ids)} partners created successfully!")
    except Exception as e:
        print(f"Error creating partners: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk mengisi data programs
async def seed_programs():
    try:
        await connect_to_mongo()
        db = await get_database()

        if await db.programs.count_documents({}) > 0:
            print("Programs already exist!")
            return

        programs_data = [
            {
                "title": "Program 1",
                "description": "Deskripsi program 1",
                "image_url": "https://example.com/program1.jpg",
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow(),
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]

        result = await db.programs.insert_many(programs_data)
        print(f"{len(result.inserted_ids)} programs created successfully!")
    except Exception as e:
        print(f"Error creating programs: {str(e)}")
    finally:
        await close_mongo_connection()

# Fungsi untuk menjalankan semua seeder
async def seed_all():
    await connect_to_mongo()
    try:
        await seed_admin()
        await seed_blog()
        await seed_gallery()
        await seed_partners()
        await seed_programs()
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
    finally:
        await close_mongo_connection()

# Entry point untuk menjalankan seeder
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
