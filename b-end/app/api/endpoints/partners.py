from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, logger, status
from fastapi.responses import JSONResponse
from app.models.schemas import PartnerBase, PartnerResponse, ResponseEnvelope
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from app.core.config import settings
from typing import List, Dict, Any
from datetime import datetime
from bson import ObjectId
import os

router = APIRouter(tags=["partners"])

def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ObjectId to string in document"""
    if doc and "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

@router.post(
    "", 
    response_model=ResponseEnvelope[PartnerResponse],
    status_code=status.HTTP_201_CREATED,
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
    name: str = Form(..., description="Nama partner/mitra", examples=["Universitas Indonesia"]),
    description: str = Form(..., description="Deskripsi partner/mitra", examples=["Mitra dalam penyelenggaraan workshop..."]),
    website_url: str = Form(..., description="URL website partner", examples=["https://www.ui.ac.id"]),
    logo: UploadFile = File(
        ..., 
        description="File logo partner (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Validasi URL
    try:
        from pydantic import HttpUrl
        HttpUrl(website_url)
    except:
        error_response = ResponseEnvelope(
            status="error",
            message="URL website tidak valid. Harap masukkan URL yang valid (contoh: https://www.example.com)"
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.model_dump()
        )
    
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
    created_partner = convert_objectid(created_partner)
    
    return ResponseEnvelope(
        status="success",
        message="Partner berhasil ditambahkan",
        data=created_partner
    )

@router.get(
    "", 
    response_model=ResponseEnvelope[List[PartnerResponse]],
    summary="Mengambil Semua Partner",
    description="Mengambil daftar semua partner/mitra."
)
async def get_partners(db=Depends(get_database)):
    partners = await db.partners.find().to_list(1000)
    partners = [convert_objectid(partner) for partner in partners]
    
    return ResponseEnvelope(
        status="success",
        message="Daftar partner berhasil diambil",
        data=partners
    )

@router.get(
    "/{partner_id}", 
    response_model=ResponseEnvelope[PartnerResponse],
    summary="Mengambil Detail Partner",
    description="Mengambil detail partner/mitra berdasarkan ID."
)
async def get_partner(partner_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(partner_id):
        error_response = ResponseEnvelope(
            status="error",
            message="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
        
    partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
    if not partner:
        error_response = ResponseEnvelope(
            status="error",
            message="Partner tidak ditemukan"
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )
    
    partner = convert_objectid(partner)
    return ResponseEnvelope(
        status="success",
        message="Detail partner berhasil diambil",
        data=partner
    )

@router.delete(
    "/{partner_id}",
    response_model=ResponseEnvelope,
    summary="Menghapus Partner",
    description="Menghapus partner/mitra berdasarkan ID."
)
async def delete_partner(
    partner_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    if not ObjectId.is_valid(partner_id):
        error_response = ResponseEnvelope(
            status="error",
            message="ID partner tidak valid. ID harus berupa 24 karakter hex string."
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
    if not partner:
        error_response = ResponseEnvelope(
            status="error",
            message="Partner tidak ditemukan"
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )
    
    # Hapus file logo jika ada
    if partner.get("logo"):
        try:
            logo_path = os.path.join(settings.STATIC_DIR, partner["logo"].lstrip("/static/"))
            if os.path.exists(logo_path):
                os.remove(logo_path)
        except Exception as e:
            logger.error(f"Error deleting logo file: {str(e)}")
    
    await db.partners.delete_one({"_id": ObjectId(partner_id)})
    
    return ResponseEnvelope(
        status="success",
        message="Partner berhasil dihapus"
    )
