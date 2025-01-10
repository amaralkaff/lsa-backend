from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query
from app.models.schemas import BlogBase, BlogResponse, ResponseEnvelope
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List, Optional
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("", response_model=BlogResponse)
async def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Handle image upload if provided
    image_url = None
    if image:
        image_url = await save_upload_file(image)
    
    blog_data = {
        "title": title,
        "content": content,
        "image_url": image_url,
        "created_at": datetime.utcnow()
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
        
        return ResponseEnvelope(
            status="success",
            message="Blogs retrieved successfully",
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
    blog = await db.blogs.find_one({"_id": ObjectId(blog_id)})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    from bson import ObjectId
    result = await db.blogs.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
