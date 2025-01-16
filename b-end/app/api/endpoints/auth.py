from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import UserCreate, UserLogin, ResponseEnvelope, Token
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.database import get_database
from app.core.config import settings
from datetime import timedelta
from fastapi.responses import JSONResponse
import logging
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
logger = logging.getLogger(__name__)


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


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    try:
        username = form_data.username.lower().strip()

        # Cari user berdasarkan email atau username
        db_user = await db.users.find_one({
            "$or": [
                {"email": username},
                {"username": username}
            ]
        })

        if not db_user:
            logger.warning(f"User not found: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Verifikasi password
        if not verify_password(form_data.password, db_user["password"]):
            logger.warning(f"Invalid password for user: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Generate access token
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
