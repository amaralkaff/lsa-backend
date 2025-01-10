from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict, List
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
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
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any,
    ) -> core_schema.CoreSchema:
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

class UserRegister(BaseModel):
    email: str = Field(
        ..., 
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Alamat email pengguna",
        example="user@example.com"
    )
    username: str = Field(
        ..., 
        min_length=3,
        description="Nama pengguna untuk login",
        example="johndoe"
    )
    password: str = Field(
        ..., 
        min_length=6,
        description="Password untuk login",
        example="secure123"
    )

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class UserLogin(BaseModel):
    email: str = Field(
        ..., 
        description="Email untuk login",
        example="user@example.com"
    )
    password: str = Field(
        ..., 
        description="Password untuk login",
        example="secure123"
    )

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    email: str = Field(
        ..., 
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Alamat email pengguna",
        example="user@example.com"
    )
    username: str = Field(
        ..., 
        min_length=3,
        description="Nama pengguna untuk login",
        example="johndoe"
    )
    is_active: bool = Field(
        default=True,
        description="Status aktif pengguna",
        exclude=True
    )
    is_admin: bool = Field(
        default=False,
        description="Status admin pengguna",
        exclude=True
    )

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=6,
        description="Password untuk login",
        example="secure123"
    )

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    username: str
    created_at: datetime

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

# Program schemas
class ProgramBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3,
        description="Judul program yang akan diselenggarakan",
        example="Workshop Pemulihan Diri"
    )
    description: str = Field(
        ...,
        description="Deskripsi lengkap tentang program",
        example="Workshop yang memberikan pemahaman dan teknik untuk pemulihan diri setelah mengalami trauma atau masalah mental"
    )
    program_type: str = Field(
        ..., 
        pattern="^(human_library|workshop|sosialisasi)$",
        description="Jenis program yang diselenggarakan",
        example="workshop"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Waktu program dibuat"
    )

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ProgramResponse(ProgramBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Blog schemas
class BlogBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3,
        description="Judul artikel blog",
        example="Pengalaman Workshop Pemulihan Mental"
    )
    content: str = Field(
        ...,
        description="Konten artikel blog",
        example="Artikel tentang pengalaman mengikuti workshop pemulihan mental dan manfaatnya"
    )
    image_url: Optional[str] = Field(
        None,
        description="URL gambar untuk artikel",
        example="https://example.com/images/workshop.jpg"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Waktu artikel dibuat"
    )
    
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class BlogResponse(BlogBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Gallery schemas
class GalleryBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3,
        description="Judul foto kegiatan",
        example="Workshop Batch 3 2023"
    )
    description: Optional[str] = Field(
        None,
        description="Deskripsi foto kegiatan",
        example="Dokumentasi kegiatan workshop pemulihan mental batch 3 tahun 2023"
    )
    image_url: str = Field(
        ...,
        description="URL foto kegiatan",
        example="https://example.com/images/gallery/workshop-batch-3.jpg"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Waktu foto diunggah"
    )
    
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class GalleryResponse(GalleryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

# Partner schemas
class PartnerBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=3,
        description="Nama mitra/partner",
        example="Universitas Indonesia"
    )
    description: Optional[str] = Field(
        None,
        description="Deskripsi tentang mitra",
        example="Mitra dalam penyelenggaraan workshop dan riset kesehatan mental"
    )
    website_url: Optional[str] = Field(
        None,
        description="URL website mitra",
        example="https://ui.ac.id"
    )
    image_url: Optional[str] = Field(
        None,
        description="URL logo mitra",
        example="https://example.com/images/partners/ui-logo.png"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Waktu mitra ditambahkan"
    )
    
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class PartnerResponse(PartnerBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class ResponseEnvelope(BaseModel):
    status: str = Field(..., description="Status response (success/error)")
    message: str = Field(..., description="Pesan response")
    data: Optional[Any] = Field(None, description="Data response")
    meta: Optional[dict] = Field(None, description="Metadata tambahan seperti pagination")
