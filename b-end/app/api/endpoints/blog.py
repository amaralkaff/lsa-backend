from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query
from app.models.schemas import BlogResponse, ResponseEnvelope
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import Optional
from datetime import datetime
import logging

router = APIRouter(tags=["blogs"])
logger = logging.getLogger(__name__)

@router.post(
    "", 
    response_model=BlogResponse,
    summary="Membuat Blog Baru",
    description="""
    Membuat blog baru dengan gambar.
    
    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
async def create_blog(
    title: str = Form(..., description="Judul blog yang akan dibuat", example="Tutorial Python"),
    content: str = Form(..., description="Konten atau isi blog", example="Python adalah bahasa pemrograman yang mudah dipelajari..."),
    image: UploadFile = File(
        ..., 
        description="File gambar untuk blog (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    """
    Membuat blog baru dengan gambar.
    
    Parameters:
    - **title**: Judul blog
    - **content**: Konten blog
    - **image**: File gambar (max 5MB, format: JPG/PNG/GIF)
    
    Returns:
    - Blog yang berhasil dibuat
    """
    # Upload gambar
    image_url = await save_upload_file(image)
    
    blog_data = {
        "title": title,
        "content": content,
        "image": image_url,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }
    
    result = await db.blogs.insert_one(blog_data)
    created_blog = await db.blogs.find_one({"_id": result.inserted_id})
    return created_blog

@router.get("", response_model=ResponseEnvelope)
async def get_blogs(
    skip: int = Query(default=0, ge=0, description="Skip n items"),
    limit: int = Query(default=10, ge=1, le=100, description="Limit the number of items"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    db = Depends(get_database)
):
    try:
        logger.info(f"Fetching blogs with skip={skip}, limit={limit}, search={search}")
        
        # Build query
        query = {}
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}}
            ]
        
        # Get total count
        total_count = await db.blogs.count_documents(query)
        
        # Get paginated results
        blogs = await db.blogs.find(query).skip(skip).limit(limit).to_list(limit)
        
        # Convert ObjectId to string
        for blog in blogs:
            blog["_id"] = str(blog["_id"])
        
        return ResponseEnvelope(
            status="success",
            message="Blog berhasil diambil",
            data=blogs,
            meta={
                "total": total_count,
                "skip": skip,
                "limit": limit,
                "has_more": (skip + limit) < total_count
            }
        )
    except Exception as e:
        logger.error(f"Error fetching blogs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: str, db=Depends(get_database)):
    from bson import ObjectId
    try:
        object_id = ObjectId(blog_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID blog tidak valid. ID harus berupa 24 karakter hex string."
        )
        
    blog = await db.blogs.find_one({"_id": object_id})
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog tidak ditemukan"
        )
    return blog

@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    from bson import ObjectId
    try:
        object_id = ObjectId(blog_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="ID blog tidak valid. ID harus berupa 24 karakter hex string."
        )
        
    result = await db.blogs.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Blog tidak ditemukan"
        )
    return {"message": "Blog berhasil dihapus"}
