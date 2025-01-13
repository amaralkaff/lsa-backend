from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from app.models.schemas import PartnerBase, PartnerResponse
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List
from datetime import datetime
from bson import ObjectId

router = APIRouter(tags=["partners"])

@router.post(
    "", 
    response_model=PartnerResponse,
    summary="Menambahkan Partner Baru",
    description="""
    Menambahkan partner/mitra baru dengan logo.
    
    **Format Logo yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
async def create_partner(
    name: str = Form(..., description="Nama partner/mitra", example="Universitas Indonesia"),
    description: str = Form(..., description="Deskripsi partner/mitra", example="Mitra dalam penyelenggaraan workshop..."),
    website_url: str = Form(..., description="URL website partner", example="https://www.ui.ac.id"),
    logo: UploadFile = File(
        ..., 
        description="File logo partner (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload logo
    logo_url = await save_upload_file(logo)
    
    partner_data = {
        "name": name,
        "description": description,
        "website_url": website_url,
        "logo": logo_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }
    
    result = await db.partners.insert_one(partner_data)
    created_partner = await db.partners.find_one({"_id": result.inserted_id})
    return created_partner

@router.get(
    "", 
    response_model=List[PartnerResponse],
    summary="Mengambil Semua Partner",
    description="Mengambil daftar semua partner/mitra."
)
async def get_partners(db=Depends(get_database)):
    partners = await db.partners.find().to_list(1000)
    return partners

@router.get(
    "/{partner_id}", 
    response_model=PartnerResponse,
    summary="Mengambil Detail Partner",
    description="Mengambil detail partner/mitra berdasarkan ID."
)
async def get_partner(partner_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(partner_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )
        
    partner = await db.partners.find_one({"_id": object_id})
    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner tidak ditemukan"
        )
    return partner

@router.delete(
    "/{partner_id}",
    summary="Menghapus Partner",
    description="Menghapus partner/mitra berdasarkan ID."
)
async def delete_partner(
    partner_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        object_id = ObjectId(partner_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )
        
    result = await db.partners.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Partner tidak ditemukan"
        )
    return {"message": "Partner berhasil dihapus"}
