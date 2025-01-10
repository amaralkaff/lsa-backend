# Panduan Lengkap Implementasi Backend FastAPI

## TAHAP 1: SETUP PROJECT & ENVIRONMENT

### Langkah 1: Setup Environment

1. Buat folder project baru

```bash
mkdir backend
cd backend
```

2. Buat virtual environment

```bash
python -m venv venv
```

3. Aktifkan virtual environment

- Windows:

```bash
venv\Scripts\activate
```

- Linux/Mac:

```bash
source venv/bin/activate
```

### Langkah 2: Install Dependencies

1. Install package utama

```bash
pip install fastapi uvicorn motor pydantic python-jose[cryptography] passlib[bcrypt] python-multipart python-decouple
```

2. Buat requirements.txt

```bash
pip freeze > requirements.txt
```

### Langkah 3: Penjelasan package utama

1. fastapi==0.104.1

   - Framework web modern dan cepat untuk membangun API
   - Berbasis Python modern (async/await)
   - Fitur validasi otomatis dan dokumentasi OpenAPI

2. uvicorn==0.24.0

   - Server ASGI yang cepat untuk menjalankan aplikasi FastAPI
   - Mendukung hot reload untuk development
   - Penanganan WebSocket

3. motor==3.3.1 & pymongo==4.5.0

   - Motor: Driver MongoDB async untuk Python
   - PyMongo: Driver MongoDB sync (diperlukan oleh Motor)
   - Menangani koneksi dan operasi database

4. python-decouple==3.8

   - Memisahkan konfigurasi dari kode
   - Membaca variabel environment
   - Memudahkan manajemen konfigurasi

5. python-multipart==0.0.6

   - Menangani form data dan file upload
   - Dibutuhkan untuk menerima request multipart/form-data
   - Penting untuk fitur upload file

6. pydantic==2.4.2

   - Validasi data dan serialisasi
   - Type hints yang powerful
   - Integrasi dengan FastAPI untuk model data

7. python-jose[cryptography]==3.3.0

   - Implementasi JWT (JSON Web Tokens)
   - Menangani enkripsi dan dekripsi token
   - Fitur keamanan untuk autentikasi

8. passlib[bcrypt]==1.7.4 & bcrypt==4.0.1

   - Passlib: Library untuk password hashing
   - Bcrypt: Algoritma hashing yang aman
   - Mengamankan password user

9. aiofiles==23.2.1
   - Operasi file async/await
   - Menangani file secara asynchronous
   - Penting untuk upload file tanpa blocking

### Langkah 4: Setup Struktur Project

1. Buat struktur folder berikut:

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── blog.py
│   │   │   ├── gallery.py
│   │   │   ├── partners.py
│   │   │   └── programs.py
│   │   └── deps.py
│   ├── core/
│   │   └── database.py
│   ├── models/
│   │   └── schemas.py
│   └── utils/
│       └── file_handler.py
├── static/
│   └── uploads/
├── main.py
├── seeder.py
└── .env
```

Saya akan menjelaskan fungsi setiap file dan folder dalam struktur proyek FastAPI ini:

### 1. Folder Root (`backend/`)

- Folder utama yang menampung seluruh proyek

### 2. Folder `app/`

- Folder inti yang berisi seluruh logika aplikasi
- Mengorganisir kode menjadi beberapa modul terpisah

### 3. Folder `app/api/`

- Berisi semua endpoint API dan dependensi
- Mengatur routing dan logika bisnis

#### 3.1 Folder `app/api/endpoints/`

- **auth.py**: Menangani autentikasi (login, register, logout)
- **blog.py**: Endpoint untuk manajemen blog/artikel
- **gallery.py**: Endpoint untuk manajemen galeri foto
- **partners.py**: Endpoint untuk manajemen mitra/partner
- **programs.py**: Endpoint untuk manajemen program/kegiatan

#### 3.2 File `app/api/deps.py`

- Berisi dependency injection
- Fungsi-fungsi helper untuk autentikasi
- Validasi token dan user

### 4. Folder `app/core/`

- Berisi komponen inti aplikasi

#### 4.1 File `app/core/database.py`

- Konfigurasi koneksi database MongoDB
- Fungsi-fungsi untuk manajemen koneksi database

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

## TAHAP 3: IMPLEMENTASI AUTHENTICATION

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
from app.models.schemas import UserRegister, UserResponse, UserLogin, Token  # Model data untuk user
from app.core.database import get_database  # Koneksi database
from datetime import datetime, timedelta  # Untuk handling waktu dan expiry token
from passlib.context import CryptContext  # Untuk hashing password
from jose import jwt  # Untuk JWT encoding/decoding
from decouple import config  # Untuk mengambil environment variables

# Inisialisasi router dan tools
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Setup password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Setup OAuth2

# Konfigurasi JWT
SECRET_KEY = config("SECRET_KEY", default="your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fungsi untuk membuat access token
def create_access_token(data: dict):
    to_encode = data.copy()
    # Set waktu expired token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode JWT dengan secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint untuk registrasi user baru
@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister, db=Depends(get_database)):
    # Cek apakah email sudah terdaftar
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # Hash password user
    hashed_password = pwd_context.hash(user.password)

    # Siapkan data user
    user_data = {
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
        "is_active": True,  # User aktif by default
        "is_admin": False,  # Bukan admin by default
        "created_at": datetime.utcnow()  # Timestamp pembuatan
    }

    # Insert user ke database
    result = await db.users.insert_one(user_data)

    # Return user yang dibuat
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return created_user

# Endpoint untuk login user
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
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
from fastapi import APIRouter, HTTPException, Depends  # Untuk routing dan error handling
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Untuk implementasi OAuth2
from app.models.schemas import UserRegister, UserResponse, UserLogin, Token  # Model data untuk user
from app.core.database import get_database  # Koneksi database
from datetime import datetime, timedelta  # Untuk handling waktu dan expiry token
from passlib.context import CryptContext  # Untuk hashing password
from jose import jwt  # Untuk JWT encoding/decoding
from decouple import config  # Untuk mengambil environment variables

# Inisialisasi router dan tools
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Setup password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Setup OAuth2

# Konfigurasi JWT
SECRET_KEY = config("SECRET_KEY", default="your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fungsi untuk membuat access token
def create_access_token(data: dict):
    to_encode = data.copy()
    # Set waktu expired token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode JWT dengan secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint untuk registrasi user baru
@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister, db=Depends(get_database)):
    # Cek apakah email sudah terdaftar
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # Hash password user
    hashed_password = pwd_context.hash(user.password)

    # Siapkan data user
    user_data = {
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
        "is_active": True,  # User aktif by default
        "is_admin": False,  # Bukan admin by default
        "created_at": datetime.utcnow()  # Timestamp pembuatan
    }

    # Insert user ke database
    result = await db.users.insert_one(user_data)

    # Return user yang dibuat
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return created_user

# Endpoint untuk login user
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
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

## TAHAP 4: IMPLEMENTASI CORE MODULES

### Langkah 1: Programs Module

1. Buat file programs.py di app/api/endpoints/:

```python
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends  # Untuk routing dan error handling
from app.models.schemas import ProgramBase, ProgramResponse  # Model data program
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_user  # Autentikasi user
from typing import List  # Untuk tipe data list
from datetime import datetime  # Untuk timestamp

# Inisialisasi router
router = APIRouter()

# Endpoint untuk membuat program baru
@router.post("", response_model=ProgramResponse)
async def create_program(
    program: ProgramBase,  # Data program dari request body
    db=Depends(get_database),  # Injeksi database connection
    current_user=Depends(get_current_user)  # Injeksi authenticated user
):
    # Konversi program ke dictionary dan tambah timestamp
    program_dict = program.model_dump()
    # Insert ke database dan return program yang dibuat
    result = await db.programs.insert_one(program_dict)
    created_program = await db.programs.find_one({"_id": result.inserted_id})
    return created_program

# Endpoint untuk mendapatkan semua program
@router.get("", response_model=List[ProgramResponse])
async def get_programs(db=Depends(get_database)):
    # Ambil semua program dari database (max 1000)
    programs = await db.programs.find().to_list(1000)
    return programs

# Endpoint untuk mendapatkan program berdasarkan ID
@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: str, db=Depends(get_database)):
    from bson import ObjectId  # Untuk konversi string ke ObjectId
    # Cari program berdasarkan ID
    program = await db.programs.find_one({"_id": ObjectId(program_id)})
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

# Endpoint untuk menghapus program
@router.delete("/{program_id}")
async def delete_program(
    program_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)  # Hanya user terautentikasi
):
    from bson import ObjectId
    # Hapus program dan cek hasilnya
    result = await db.programs.delete_one({"_id": ObjectId(program_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}
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
from app.models.schemas import BlogBase, BlogResponse, ResponseEnvelope  # Model data untuk blog
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_user  # Autentikasi user
from app.utils.file_handler import save_upload_file  # Fungsi untuk menyimpan file
from typing import List, Optional  # Tipe data list dan opsional
from datetime import datetime  # Untuk timestamp
import logging  # Untuk logging

# Inisialisasi router dan logger
router = APIRouter()
logger = logging.getLogger(__name__)

# Endpoint untuk membuat blog baru
@router.post("", response_model=BlogResponse)
async def create_blog(
    title: str = Form(...),  # Judul blog (required)
    content: str = Form(...),  # Konten blog (required)
    image: Optional[UploadFile] = File(None),  # Gambar blog (optional)
    db=Depends(get_database),  # Injeksi database
    current_user=Depends(get_current_user)  # Injeksi user yang terautentikasi
):
    # Simpan gambar jika ada
    image_url = None
    if image:
        image_url = await save_upload_file(image)

    # Siapkan data blog
    blog_data = {
        "title": title,
        "content": content,
        "image_url": image_url,
        "created_at": datetime.utcnow()  # Tambah timestamp
    }

    # Insert ke database dan return blog yang dibuat
    result = await db.blogs.insert_one(blog_data)
    created_blog = await db.blogs.find_one({"_id": result.inserted_id})
    return created_blog

# Endpoint untuk mendapatkan daftar blog dengan paginasi dan pencarian
@router.get("", response_model=ResponseEnvelope)
async def get_blogs(
    skip: int = Query(default=0, ge=0, description="Skip n items"),  # Untuk paginasi
    limit: int = Query(default=10, ge=1, le=100, description="Limit the number of items"),  # Batasan item per halaman
    search: Optional[str] = Query(None, description="Search in title and content"),  # Kata kunci pencarian
    db = Depends(get_database)
):
    try:
        logger.info(f"Fetching blogs with skip={skip}, limit={limit}, search={search}")

        # Buat query pencarian jika ada kata kunci
        query = {}
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},  # Cari di judul
                {"content": {"$regex": search, "$options": "i"}}  # Cari di konten
            ]

        # Hitung total dokumen
        total_count = await db.blogs.count_documents(query)

        # Ambil data dengan paginasi
        blogs = await db.blogs.find(query).skip(skip).limit(limit).to_list(limit)

        # Return response dengan metadata
        return ResponseEnvelope(
            status="success",
            message="Blogs retrieved successfully",
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
    from bson import ObjectId  # Untuk konversi string ke ObjectId
    # Cari blog berdasarkan ID
    blog = await db.blogs.find_one({"_id": ObjectId(blog_id)})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# Endpoint untuk menghapus blog
@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)  # Hanya user terautentikasi
):
    from bson import ObjectId
    # Hapus blog dan cek hasilnya
    result = await db.blogs.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
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

1. Implementasi gallery endpoints dengan file upload:

```python
# Import library yang diperlukan
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File  # Untuk routing dan handling HTTP
from app.models.schemas import GalleryBase, GalleryResponse  # Model data untuk galeri
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_user  # Autentikasi user
from app.utils.file_handler import save_upload_file  # Fungsi untuk menyimpan file
from typing import List  # Tipe data list
from datetime import datetime  # Untuk timestamp

# Inisialisasi router
router = APIRouter()

# Endpoint untuk membuat galeri baru
@router.post("", response_model=GalleryResponse)
async def create_gallery(
    title: str = Form(...),  # Judul galeri (required)
    description: str = Form(None),  # Deskripsi galeri (optional)
    image: UploadFile = File(...),  # File gambar (required)
    db=Depends(get_database),  # Injeksi database
    current_user=Depends(get_current_user)  # Injeksi user yang terautentikasi
):
    # Simpan file gambar dan dapatkan URL-nya
    image_url = await save_upload_file(image)

    # Siapkan data galeri yang akan disimpan
    gallery_data = {
        "title": title,
        "description": description,
        "image_url": image_url,
        "created_at": datetime.utcnow()  # Tambah timestamp
    }

    # Insert ke database dan return galeri yang dibuat
    result = await db.gallery.insert_one(gallery_data)
    created_gallery = await db.gallery.find_one({"_id": result.inserted_id})
    return created_gallery

# Endpoint untuk mendapatkan semua galeri
@router.get("", response_model=List[GalleryResponse])
async def get_galleries(db=Depends(get_database)):
    # Ambil semua galeri dari database (max 1000)
    galleries = await db.gallery.find().to_list(1000)
    return galleries

# Endpoint untuk mendapatkan galeri berdasarkan ID
@router.get("/{gallery_id}", response_model=GalleryResponse)
async def get_gallery(gallery_id: str, db=Depends(get_database)):
    from bson import ObjectId  # Untuk konversi string ke ObjectId
    # Cari galeri berdasarkan ID
    gallery = await db.gallery.find_one({"_id": ObjectId(gallery_id)})
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return gallery

# Endpoint untuk menghapus galeri
@router.delete("/{gallery_id}")
async def delete_gallery(
    gallery_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)  # Hanya user terautentikasi
):
    from bson import ObjectId
    # Hapus galeri dan cek hasilnya
    result = await db.gallery.delete_one({"_id": ObjectId(gallery_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return {"message": "Gallery deleted successfully"}
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
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File  # Untuk routing dan handling HTTP
from app.models.schemas import PartnerBase, PartnerResponse  # Model data untuk partner
from app.core.database import get_database  # Koneksi database
from app.api.deps import get_current_user  # Autentikasi user
from app.utils.file_handler import save_upload_file  # Fungsi untuk menyimpan file
from typing import List, Optional  # Tipe data list dan opsional
from datetime import datetime  # Untuk timestamp

# Inisialisasi router
router = APIRouter()

# Endpoint untuk membuat partner baru
@router.post("", response_model=PartnerResponse)
async def create_partner(
    name: str = Form(...),  # Nama partner (required)
    description: str = Form(None),  # Deskripsi partner (optional)
    website_url: str = Form(None),  # URL website partner (optional)
    image: Optional[UploadFile] = File(None),  # Logo partner (optional)
    db=Depends(get_database),  # Injeksi database
    current_user=Depends(get_current_user)  # Injeksi user yang terautentikasi
):
    # Simpan gambar jika ada
    image_url = None
    if image:
        image_url = await save_upload_file(image)

    # Siapkan data partner
    partner_data = {
        "name": name,
        "description": description,
        "website_url": website_url,
        "image_url": image_url,
        "created_at": datetime.utcnow()  # Tambah timestamp
    }

    # Insert ke database dan return partner yang dibuat
    result = await db.partners.insert_one(partner_data)
    created_partner = await db.partners.find_one({"_id": result.inserted_id})
    return created_partner

# Endpoint untuk mendapatkan semua partner
@router.get("", response_model=List[PartnerResponse])
async def get_partners(db=Depends(get_database)):
    # Ambil semua partner dari database (max 1000)
    partners = await db.partners.find().to_list(1000)
    return partners

# Endpoint untuk mendapatkan partner berdasarkan ID
@router.get("/{partner_id}", response_model=PartnerResponse)
async def get_partner(partner_id: str, db=Depends(get_database)):
    from bson import ObjectId  # Untuk konversi string ke ObjectId
    # Cari partner berdasarkan ID
    partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner

# Endpoint untuk menghapus partner
@router.delete("/{partner_id}")
async def delete_partner(
    partner_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)  # Hanya user terautentikasi
):
    from bson import ObjectId
    # Hapus partner dan cek hasilnya
    result = await db.partners.delete_one({"_id": ObjectId(partner_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner deleted successfully"}
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

## TAHAP 5: SETUP MAIN APPLICATION

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

## TAHAP 6: TESTING API ENDPOINTS

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

## TAHAP 7: DOKUMENTASI API

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
            "description": "Operations with user authentication"
        },
        {
            "name": "programs",
            "description": "CRUD operations for programs"
        },
        {
            "name": "blogs",
            "description": "Blog management endpoints"
        },
        {
            "name": "gallery",
            "description": "Gallery management endpoints"
        },
        {
            "name": "partners",
            "description": "Partner management endpoints"
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

## TAHAP 8: SECURITY ENHANCEMENTS

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

## TAHAP 9: DEPLOYMENT PREPARATION

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

## FINAL CHECKLIST

### Security Checklist:

- [ ] Authentication working
- [ ] Password hashing implemented
- [ ] JWT token secure
- [ ] CORS configured
- [ ] Rate limiting active
- [ ] File upload validation
- [ ] Error handling complete

### Functionality Checklist:

- [ ] All CRUD operations working
- [ ] File uploads functioning
- [ ] Database connections stable
- [ ] Endpoints documented
- [ ] Testing complete
- [ ] Seeder working

### Deployment Checklist:

- [ ] Environment variables set
- [ ] Docker configuration complete
- [ ] Database backup strategy
- [ ] Monitoring setup
- [ ] Logging configured
- [ ] SSL/TLS ready

## MAINTENANCE TIPS

1. Regular Maintenance:

   - Monitor error logs
   - Check database performance
   - Update dependencies
   - Backup database regularly

2. Scaling Considerations:

   - Monitor API usage
   - Optimize database queries
   - Consider caching
   - Load balancing setup

3. Security Updates:

   - Regular security audits
   - Update dependencies
   - Monitor for vulnerabilities
   - Keep backups secure

4. Feature Additions
   - User roles
   - API versioning
   - Webhook support

## Webhook Support

### Webhook Configuration

```javascript
{
  _id: ObjectId,
  url: String,           // Required, webhook destination URL
  event_type: String,    // Required, event to listen for
  is_active: Boolean,    // Default: true
  secret_key: String,    // Optional, for webhook signature
  created_at: DateTime   // Auto-generated
}
```

### Supported Events

1. Content Updates

   - program.created
   - program.updated
   - program.deleted
   - blog.created
   - blog.updated
   - blog.deleted

2. User Events

   - user.registered
   - user.login
   - user.status_changed

3. System Events
   - system.backup_completed
   - system.error_occurred

### Webhook Security

1. Signature Verification

```python
def generate_webhook_signature(payload: dict, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256
    ).hexdigest()
```

2. Retry Mechanism

```python
WEBHOOK_RETRY_ATTEMPTS = 3
WEBHOOK_RETRY_DELAY = 60  # seconds
```

3. Security Best Practices
   - HTTPS Only
   - Signature Verification
   - Rate Limiting
   - Timeout Configuration
   - IP Whitelisting

### Example Webhook Payload

```javascript
{
  "event_type": "program.created",
  "timestamp": "2024-01-10T12:00:00Z",
  "data": {
    "program_id": "123",
    "title": "New Program",
    "description": "Program Description"
  },
  "signature": "sha256_hash_signature"
}
```

### Webhook Management API

1. Register Webhook

```http
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://example.com/webhook",
  "event_type": "program.created",
  "secret_key": "optional_secret"
}
```

2. List Webhooks

```http
GET /api/webhooks
```

3. Update Webhook

```http
PUT /api/webhooks/{webhook_id}
```

4. Delete Webhook

```http
DELETE /api/webhooks/{webhook_id}
```

### Webhook Implementation

```python
async def trigger_webhook(event_type: str, payload: dict):
    webhooks = await db.webhooks.find({
        "event_type": event_type,
        "is_active": True
    }).to_list(None)

    for webhook in webhooks:
        try:
            if webhook.get("secret_key"):
                signature = generate_webhook_signature(
                    payload,
                    webhook["secret_key"]
                )
                headers = {"X-Webhook-Signature": signature}
            else:
                headers = {}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook["url"],
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status >= 400:
                        # Handle failed delivery
                        await log_webhook_failure(webhook, payload, response)

        except Exception as e:
            # Log error and schedule retry
            await schedule_webhook_retry(webhook, payload)
```

### Best Practices

1. Payload Design

   - Keep payloads small and focused
   - Include only necessary data
   - Maintain consistent structure
   - Version your webhook payloads

2. Error Handling

   - Implement retry mechanism
   - Log failed deliveries
   - Monitor webhook health
   - Alert on repeated failures

3. Performance

   - Async webhook processing
   - Batch similar events
   - Implement rate limiting
   - Use webhook queues

4. Monitoring
   - Track delivery success rates
   - Monitor response times
   - Alert on high failure rates
   - Log detailed error information
