import os
import shutil
from fastapi import UploadFile, HTTPException
from datetime import datetime
import uuid

UPLOAD_DIR = "static/uploads"

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
            detail="File type not allowed. Only JPEG, PNG and GIF are allowed"
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}_{unique_id}{file_extension}"
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
    finally:
        file.file.close()
    
    return f"/{UPLOAD_DIR}/{filename}"
