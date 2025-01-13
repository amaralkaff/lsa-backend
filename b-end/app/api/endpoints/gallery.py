from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from app.models.schemas import GalleryBase, GalleryResponse
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List
from datetime import datetime
from bson import ObjectId

router = APIRouter(tags=["gallery"])

@router.post(
    "", 
    response_model=GalleryResponse,
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
    title: str = Form(..., description="Judul foto", example="Workshop Batch 2023"),
    description: str = Form(..., description="Deskripsi foto", example="Dokumentasi kegiatan workshop..."),
    image: UploadFile = File(
        ..., 
        description="File foto (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload gambar
    image_url = await save_upload_file(image)
    
    gallery_data = {
        "title": title,
        "description": description,
        "image": image_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }
    
    result = await db.gallery.insert_one(gallery_data)
    created_gallery = await db.gallery.find_one({"_id": result.inserted_id})
    return created_gallery

@router.get(
    "", 
    response_model=List[GalleryResponse],
    summary="Mengambil Semua Foto Galeri",
    description="Mengambil daftar semua foto yang ada di galeri."
)
async def get_galleries(db=Depends(get_database)):
    galleries = await db.gallery.find().to_list(1000)
    return galleries

@router.get(
    "/{gallery_id}", 
    response_model=GalleryResponse,
    summary="Mengambil Detail Foto",
    description="Mengambil detail foto berdasarkan ID."
)
async def get_gallery(gallery_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(gallery_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID galeri tidak valid. ID harus berupa 24 karakter hex string."
        )
        
    gallery = await db.gallery.find_one({"_id": object_id})
    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Foto tidak ditemukan"
        )
    return gallery

@router.delete(
    "/{gallery_id}",
    summary="Menghapus Foto",
    description="Menghapus foto dari galeri berdasarkan ID."
)
async def delete_gallery(
    gallery_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        object_id = ObjectId(gallery_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID galeri tidak valid. ID harus berupa 24 karakter hex string."
        )
        
    result = await db.gallery.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Foto tidak ditemukan"
        )
    return {"message": "Foto berhasil dihapus"}
