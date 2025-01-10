from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from app.models.schemas import PartnerBase, PartnerResponse
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.post("", response_model=PartnerResponse)
async def create_partner(
    name: str = Form(...),
    description: str = Form(None),
    website_url: str = Form(None),
    image: Optional[UploadFile] = File(None),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Handle optional image upload
    image_url = None
    if image:
        image_url = await save_upload_file(image)
    
    partner_data = {
        "name": name,
        "description": description,
        "website_url": website_url,
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }
    
    result = await db.partners.insert_one(partner_data)
    created_partner = await db.partners.find_one({"_id": result.inserted_id})
    return created_partner

@router.get("", response_model=List[PartnerResponse])
async def get_partners(db=Depends(get_database)):
    partners = await db.partners.find().to_list(1000)
    return partners

@router.get("/{partner_id}", response_model=PartnerResponse)
async def get_partner(partner_id: str, db=Depends(get_database)):
    from bson import ObjectId
    partner = await db.partners.find_one({"_id": ObjectId(partner_id)})
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner

@router.delete("/{partner_id}")
async def delete_partner(
    partner_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    from bson import ObjectId
    result = await db.partners.delete_one({"_id": ObjectId(partner_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner deleted successfully"}
