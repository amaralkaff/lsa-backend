from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import UserCreate, UserLogin, ResponseEnvelope, Token
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.database import get_database
from app.core.config import settings
from datetime import timedelta
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/register", response_model=ResponseEnvelope, status_code=201)
async def register(user: UserCreate, db=Depends(get_database)):
    # Cek apakah email sudah terdaftar
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        return JSONResponse(
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
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "message": "Username already taken",
                "data": None,
                "meta": None
            }
        )

    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Simpan user baru
    user_data = {
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "password": hashed_password,
        "is_active": True
    }
    
    result = await db.users.insert_one(user_data)
    
    # Return user data tanpa password
    user_response = {
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "is_active": True,
        "id": str(result.inserted_id)
    }
    
    return ResponseEnvelope(
        status="success",
        message="User registered successfully",
        data=user_response,
        meta=None
    )

@router.post("/login", response_model=ResponseEnvelope)
async def login(user: UserLogin, db=Depends(get_database)):
    # Cari user berdasarkan email
    db_user = await db.users.find_one({"email": user.email})
    if not db_user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": "User not found",
                "data": None,
                "meta": None
            }
        )

    # Verifikasi password
    if not verify_password(user.password, db_user["password"]):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "error",
                "message": "Incorrect password",
                "data": None,
                "meta": None
            }
        )

    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["email"]},
        expires_delta=access_token_expires
    )

    return ResponseEnvelope(
        status="success",
        message="Login successful",
        data={"access_token": access_token, "token_type": "bearer"},
        meta=None
    ) 