from datetime import datetime
from typing import Optional, Any, Annotated, TypeVar, Generic
from pydantic import BaseModel, Field, ConfigDict, HttpUrl, EmailStr, BeforeValidator
from bson import ObjectId

# Fungsi validator untuk ObjectId


def validate_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError("Invalid ObjectId")


# Tipe kustom untuk ObjectId
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]

# Generic type untuk ResponseEnvelope
T = TypeVar('T')

# Model untuk Program


class ProgramBase(BaseModel):
    title: str = Field(..., min_length=3, description="Judul program")
    subtitle: str = Field(..., min_length=3, description="Sub judul program")
    description: str = Field(..., description="Deskripsi lengkap program")
    image: str = Field(..., description="URL gambar program")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Waktu pembuatan")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Workshop Data Science",
                "subtitle": "Pengenalan Data Science untuk Pemula",
                "description": "Workshop pengenalan data science untuk pemula",
                "image": "/static/uploads/program1.jpg"
            }
        }
    )


class ProgramResponse(ProgramBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

# Model untuk Blog


class BlogBase(BaseModel):
    title: str = Field(..., min_length=3, description="Judul blog")
    content: str = Field(..., description="Konten blog")
    image: str = Field(..., description="URL gambar blog")
    author: str = Field(..., description="Email pembuat blog")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Waktu pembuatan")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Pengenalan Data Science",
                "content": "Data science adalah...",
                "image": "/static/uploads/blog1.jpg",
                "author": "admin@example.com"
            }
        }
    )


class BlogResponse(BlogBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

# Model untuk Gallery


class GalleryBase(BaseModel):
    title: Optional[str] = Field(None, description="Judul foto")
    description: Optional[str] = Field(None, description="Deskripsi foto")
    image: str = Field(..., description="URL foto")
    author: str = Field(..., description="Email pengunggah foto")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Waktu unggah")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Workshop Data Science 2024",
                "description": "Dokumentasi workshop data science",
                "image": "/static/uploads/gallery1.jpg",
                "author": "admin@example.com"
            }
        }
    )


class GalleryResponse(GalleryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

# Model untuk Partner


class PartnerBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nama partner/mitra")
    description: Optional[str] = Field(None, min_length=10,
                                       description="Deskripsi partner/mitra")
    website_url: HttpUrl = Field(..., description="URL website partner")
    logo: str = Field(..., description="URL logo partner")
    author: str = Field(..., description="Email penambah partner")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Waktu penambahan")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "Tech Company",
                "description": "Perusahaan teknologi terkemuka",
                "website_url": "https://example.com",
                "logo": "/static/uploads/partner1.jpg",
                "author": "admin@example.com"
            }
        }
    )


class PartnerResponse(PartnerBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

# Model untuk Response Envelope


class ResponseEnvelope(BaseModel, Generic[T]):
    status: str = Field(..., description="Status response (success/error)")
    message: str = Field(..., description="Pesan response")
    data: Optional[T] = Field(None, description="Data response")
    meta: Optional[dict] = Field(None, description="Metadata response")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "Data berhasil diambil",
                "data": None,
                "meta": None
            }
        }
    )

# Model untuk Token


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None
    username: Optional[str] = None

# Model untuk User


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email user")
    username: str = Field(..., min_length=3,
                          description="Username untuk login")
    full_name: str = Field(..., min_length=3, description="Nama lengkap user")
    is_active: bool = Field(default=True, description="Status aktif user")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Waktu pendaftaran")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True
            }
        }
    )


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email user")
    username: str = Field(..., min_length=3,
                          description="Username untuk login")
    full_name: str = Field(..., min_length=3, description="Nama lengkap user")
    password: str = Field(..., min_length=8, description="Password user")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "secretpassword"
            }
        }
    )


class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "secretpassword"
            }
        }
    )


class UserResponse(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
