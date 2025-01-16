from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, status
from fastapi.responses import JSONResponse
from app.models.schemas import GalleryBase, GalleryResponse, ResponseEnvelope
from app.core.database import get_database
from app.api.deps import get_current_active_user, get_current_user
from app.utils.file_handler import save_upload_file
from app.core.config import settings
from typing import List, Dict, Any
from datetime import datetime
from bson import ObjectId
import os

router = APIRouter(tags=["gallery"])

def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ObjectId to string in document"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post(
    "", 
    response_model=ResponseEnvelope[GalleryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Menambahkan Foto ke Galeri",
    description="""
    Menambahkan foto baru ke galeri.
    
    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
async def create_gallery(
    title: str = Form(None, description="Judul foto", examples=["Workshop Batch 2023"]),
    description: str = Form(None, description="Deskripsi foto", examples=["Dokumentasi kegiatan workshop..."]),
    image: UploadFile = File(
        ..., 
        description="File foto (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        # Upload gambar
        image_url = await save_upload_file(image)
        
        gallery_data = {
            "title": title or "",
            "description": description or "",
            "image": image_url,
            "created_at": datetime.utcnow(),
            "author": current_user["email"]
        }
        
        result = await db.gallery.insert_one(gallery_data)
        created_gallery = await db.gallery.find_one({"_id": result.inserted_id})
        created_gallery = convert_objectid(created_gallery)
        
        return ResponseEnvelope[GalleryResponse](
            status="success",
            message="Foto berhasil ditambahkan",
            data=created_gallery
        )
    except Exception as e:
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

@router.get(
    "", 
    response_model=ResponseEnvelope[List[GalleryResponse]],
    summary="Mengambil Semua Foto Galeri",
    description="Mengambil daftar semua foto yang ada di galeri."
)
async def get_galleries(db=Depends(get_database)):
    try:
        galleries = await db.gallery.find().to_list(1000)
        galleries = [convert_objectid(gallery) for gallery in galleries]
        
        return ResponseEnvelope[List[GalleryResponse]](
            status="success",
            message="Daftar foto berhasil diambil",
            data=galleries
        )
    except Exception as e:
        error_response = ResponseEnvelope(
            status="error",
            message=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )

@router.get("/{gallery_id}", response_model=ResponseEnvelope)
async def get_gallery(gallery_id: str, db = Depends(get_database)):
    """Mengambil detail foto berdasarkan ID"""
    try:
        if not ObjectId.is_valid(gallery_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID foto tidak valid",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_response.dict())

        gallery = await db.gallery.find_one({"_id": ObjectId(gallery_id)})
        if not gallery:
            error_response = ResponseEnvelope(
                status="error",
                message="Foto tidak ditemukan",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_response.model_dump())

        gallery = convert_objectid(gallery)
        return ResponseEnvelope(
            status="success",
            message="Detail foto berhasil diambil",
            data=gallery
        )
    except Exception as e:
        error_response = ResponseEnvelope(
            status="error",
            message=str(e),
            data=None
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.dict())

@router.delete("/{gallery_id}", response_model=ResponseEnvelope)
async def delete_gallery(gallery_id: str, current_user = Depends(get_current_user), db = Depends(get_database)):
    """Menghapus foto berdasarkan ID"""
    try:
        if not ObjectId.is_valid(gallery_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID foto tidak valid",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_response.dict())

        gallery = await db.gallery.find_one({"_id": ObjectId(gallery_id)})
        if not gallery:
            error_response = ResponseEnvelope(
                status="error",
                message="Foto tidak ditemukan",
                data=None
            )
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_response.dict())

        # Hapus file foto
        if gallery.get("image"):
            image_path = os.path.join(settings.STATIC_DIR, gallery["image"].lstrip("/static/"))
            if os.path.exists(image_path):
                os.remove(image_path)

        # Hapus data dari database
        await db.gallery.delete_one({"_id": ObjectId(gallery_id)})

        return ResponseEnvelope(
            status="success",
            message="Foto berhasil dihapus",
            data=None
        )
    except Exception as e:
        error_response = ResponseEnvelope(
            status="error",
            message=str(e),
            data=None
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.dict())
