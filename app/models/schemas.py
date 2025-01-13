from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import HttpUrl

# Custom class untuk validasi ObjectId
class PyObjectId:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(lambda x: ObjectId(x)),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

# Model untuk Authentication
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    is_admin: bool = False

class UserLogin(BaseModel):
    email: str = Field(..., email=True)
    password: str = Field(..., min_length=6)

# Model untuk User
class UserRegister(BaseModel):
    email: str = Field(
        ..., 
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Email harus valid",
        examples=["user@example.com"]
    )
    username: str = Field(
        ..., 
        min_length=3,
        description="Username minimal 3 karakter",
        examples=["johndoe"]
    )
    password: str = Field(
        ..., 
        min_length=6,
        description="Password minimal 6 karakter",
        examples=["strongpassword123"]
    )

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    email: str
    username: str
    created_at: datetime
    is_active: bool = True
    is_admin: bool = False
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

# Model untuk Program
class ProgramBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    program_type: str = Field(..., pattern="^(human_library|workshop|sosialisasi)$")
    image: str
    start_date: datetime
    end_date: datetime
    author: str = Field(..., description="Email dari user yang membuat program")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProgramResponse(ProgramBase):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

# Model untuk Blog
class BlogBase(BaseModel):
    title: str = Field(..., min_length=3)
    content: str
    image: str
    author: str = Field(..., description="Email dari user yang membuat blog")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BlogResponse(BlogBase):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

# Model untuk Gallery
class GalleryBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    image: str
    author: str = Field(..., description="Email dari user yang mengupload foto")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GalleryResponse(GalleryBase):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

# Model untuk Partner
class PartnerBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nama partner/mitra")
    description: str = Field(..., min_length=10, description="Deskripsi partner/mitra")
    website_url: HttpUrl = Field(..., description="URL website partner")
    logo: str
    author: str = Field(..., description="Email dari user yang menambahkan partner")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PartnerResponse(PartnerBase):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

# Model untuk Response Envelope
class ResponseEnvelope(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
    meta: Optional[dict] = None
