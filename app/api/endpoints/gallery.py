from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from app.models.schemas import GalleryBase, GalleryResponse
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("", response_model=GalleryResponse)
async def create_gallery(
    title: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(...),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Handle image upload (required for gallery)
    image_url = await save_upload_file(image)
    
    gallery_data = {
        "title": title,
        "description": description,
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }
    
    result = await db.gallery.insert_one(gallery_data)
    created_gallery = await db.gallery.find_one({"_id": result.inserted_id})
    return created_gallery

@router.get("", response_model=List[GalleryResponse])
async def get_galleries(db=Depends(get_database)):
    galleries = await db.gallery.find().to_list(1000)
    return galleries

@router.get("/{gallery_id}", response_model=GalleryResponse)
async def get_gallery(gallery_id: str, db=Depends(get_database)):
    from bson import ObjectId
    gallery = await db.gallery.find_one({"_id": ObjectId(gallery_id)})
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return gallery

@router.delete("/{gallery_id}")
async def delete_gallery(
    gallery_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    from bson import ObjectId
    result = await db.gallery.delete_one({"_id": ObjectId(gallery_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return {"message": "Gallery deleted successfully"}
