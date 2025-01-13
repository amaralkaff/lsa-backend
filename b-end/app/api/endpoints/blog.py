from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.models.schemas import BlogBase, BlogResponse, ResponseEnvelope
from app.api.deps import get_current_user
from app.utils.file_handler import save_upload_file

router = APIRouter()

def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ObjectId to string in document"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("", response_model=ResponseEnvelope[BlogResponse], status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """Create a new blog"""
    try:
        # Save image if provided
        image_path = await save_upload_file(image)
            
        blog_data = {
            "title": title,
            "content": content,
            "image": image_path,
            "author": current_user["email"],
            "created_at": datetime.utcnow()
        }
        
        result = await db["blogs"].insert_one(blog_data)
        
        # Get created blog
        created_blog = await db["blogs"].find_one({"_id": result.inserted_id})
        created_blog = convert_objectid(created_blog)
        
        return ResponseEnvelope[BlogResponse](
            status="success",
            message="Blog berhasil dibuat",
            data=created_blog
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

@router.get("", response_model=ResponseEnvelope[List[BlogResponse]])
async def get_blogs(db = Depends(get_database)):
    """Get all blogs"""
    try:
        blogs = await db["blogs"].find().to_list(None)
        blogs = [convert_objectid(blog) for blog in blogs]
        
        return ResponseEnvelope[List[BlogResponse]](
            status="success",
            message="Daftar blog berhasil diambil",
            data=blogs
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

@router.get("/{blog_id}", response_model=ResponseEnvelope[BlogResponse])
async def get_blog(blog_id: str, db = Depends(get_database)):
    """Get a blog by ID"""
    try:
        if not ObjectId.is_valid(blog_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID blog tidak valid"
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response.model_dump()
            )
            
        blog = await db["blogs"].find_one({"_id": ObjectId(blog_id)})
        if not blog:
            error_response = ResponseEnvelope(
                status="error",
                message="Blog tidak ditemukan"
            )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=error_response.model_dump()
            )
            
        blog = convert_objectid(blog)
        return ResponseEnvelope[BlogResponse](
            status="success",
            message="Detail blog berhasil diambil",
            data=blog
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

@router.delete("/{blog_id}", response_model=ResponseEnvelope)
async def delete_blog(blog_id: str, current_user = Depends(get_current_user), db = Depends(get_database)):
    """Delete a blog"""
    try:
        if not ObjectId.is_valid(blog_id):
            error_response = ResponseEnvelope(
                status="error",
                message="ID blog tidak valid"
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response.model_dump()
            )
            
        blog = await db["blogs"].find_one({"_id": ObjectId(blog_id)})
        if not blog:
            error_response = ResponseEnvelope(
                status="error",
                message="Blog tidak ditemukan"
            )
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=error_response.model_dump()
            )
            
        # Check if user is author
        if blog["author"] != current_user["email"]:
            error_response = ResponseEnvelope(
                status="error",
                message="Anda tidak memiliki akses untuk menghapus blog ini"
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=error_response.model_dump()
            )
            
        await db["blogs"].delete_one({"_id": ObjectId(blog_id)})
        return ResponseEnvelope(
            status="success",
            message="Blog berhasil dihapus"
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
