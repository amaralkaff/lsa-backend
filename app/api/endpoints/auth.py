from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.schemas import UserResponse, Token, UserRegister
from app.core.database import get_database
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

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
    # Check if user exists
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Prepare user data
    user_data = {
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow()
    }
    
    # Insert user
    result = await db.users.insert_one(user_data)
    
    # Get created user
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return created_user

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
    user = await db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Email atau password salah")
    
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Email atau password salah")
    
    if not user.get("is_active", False):
        raise HTTPException(status_code=400, detail="Akun tidak aktif")
    
    access_token = create_access_token(
        data={"sub": user["email"], "is_admin": user.get("is_admin", False)}
    )
    return {"access_token": access_token, "token_type": "bearer"} 