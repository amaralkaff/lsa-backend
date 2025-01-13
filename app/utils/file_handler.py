import os
import shutil
from fastapi import UploadFile, HTTPException
from datetime import datetime
import uuid

UPLOAD_DIR = "static/uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Pastikan direktori upload ada
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
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
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = os.path.splitext(file.filename)[1].lower()
    if not file_extension:
        file_extension = ".jpg"  # Default extension
    filename = f"{timestamp}_{unique_id}{file_extension}"
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal mengunggah file: {str(e)}"
        )
    finally:
        file.file.close()
    
    return f"/{UPLOAD_DIR}/{filename}"
