from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from bson import ObjectId
from .schemas import PyObjectId

class Token(BaseModel):
    """Model untuk token autentikasi."""
    access_token: str = Field(..., description="Token akses JWT")
    token_type: str = Field(default="bearer", description="Tipe token")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )

class TokenData(BaseModel):
    """Model untuk data yang disimpan dalam token."""
    email: Optional[str] = Field(None, description="Email pengguna")
    is_admin: bool = Field(default=False, description="Status admin")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "is_admin": False
            }
        }
    )

class UserLogin(BaseModel):
    """Model untuk login pengguna."""
    email: EmailStr = Field(..., description="Email pengguna")
    password: str = Field(..., min_length=6, description="Password pengguna")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }
    )

class UserRegister(BaseModel):
    """Model untuk registrasi pengguna baru."""
    email: EmailStr = Field(..., description="Email pengguna")
    username: str = Field(
        ..., 
        min_length=3,
        description="Username minimal 3 karakter"
    )
    password: str = Field(
        ..., 
        min_length=6,
        description="Password minimal 6 karakter"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "strongpassword123"
            }
        }
    )

class UserResponse(BaseModel):
    """Model untuk response data pengguna."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(..., description="Email pengguna")
    username: str = Field(..., description="Username pengguna")
    created_at: datetime = Field(..., description="Waktu pembuatan akun")
    is_active: bool = Field(default=True, description="Status aktif")
    is_admin: bool = Field(default=False, description="Status admin")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "username": "johndoe",
                "created_at": "2024-01-01T00:00:00",
                "is_active": True,
                "is_admin": False
            }
        }
    ) 