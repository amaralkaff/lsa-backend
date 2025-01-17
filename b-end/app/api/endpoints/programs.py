from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query, status
from fastapi.responses import JSONResponse
from app.models.schemas import ProgramBase, ProgramResponse, ResponseEnvelope
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List, Literal, Union, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from enum import Enum


class ProgramType(str, Enum):
    ALL = "all"
    HUMAN_LIBRARY = "human_library"
    WORKSHOP = "workshop"
    SOSIALISASI = "sosialisasi"
    SEMINAR = "seminar"
    TRAINING = "training"


router = APIRouter(tags=["programs"])


def convert_objectid(doc: Dict[str, Any]) -> Dict[str, Any]:
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


@router.post(
    "",
    response_model=ResponseEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Membuat Program Baru",
    description="""
    Membuat program baru dengan gambar.
    
    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    """
)
async def create_program(
    title: str = Form(..., description="Judul program",
                      examples=["Workshop Pemulihan Mental"]),
    subtitle: str = Form(..., description="Sub judul program", examples=[
                         "Mengenal Lebih Dalam tentang Kesehatan Mental"]),
    description: str = Form(..., description="Deskripsi program", examples=[
                            "Workshop untuk pemulihan kesehatan mental..."]),
    image: UploadFile = File(
        ...,
        description="File gambar untuk program (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload gambar
    image_url = await save_upload_file(image)

    program_data = {
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "image": image_url,
        "created_at": datetime.utcnow()
    }

    # Validate program data using ProgramBase
    program = ProgramBase(**program_data)

    result = await db.programs.insert_one(program.model_dump())
    created_program = await db.programs.find_one({"_id": result.inserted_id})
    created_program = convert_objectid(created_program)

    return ResponseEnvelope(
        status="success",
        message="Program berhasil dibuat",
        data=created_program
    )


@router.get(
    "",
    response_model=ResponseEnvelope,
    summary="Mengambil Semua Program",
    description="Mengambil daftar program yang tersedia."
)
async def get_programs(
    db=Depends(get_database)
):
    programs = await db.programs.find().to_list(1000)
    programs = [convert_objectid(program) for program in programs]

    return ResponseEnvelope(
        status="success",
        message="Daftar program berhasil diambil",
        data=programs
    )


@router.get(
    "/{program_id}",
    response_model=ResponseEnvelope,
    summary="Mengambil Detail Program",
    description="Mengambil detail program berdasarkan ID."
)
async def get_program(program_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        error_response = ResponseEnvelope(
            status="error",
            message="ID program tidak valid. ID harus berupa 24 karakter hex string.",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )

    program = await db.programs.find_one({"_id": object_id})
    if not program:
        error_response = ResponseEnvelope(
            status="error",
            message="Program tidak ditemukan",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )

    program = convert_objectid(program)
    return ResponseEnvelope(
        status="success",
        message="Detail program berhasil diambil",
        data=program
    )


@router.delete(
    "/{program_id}",
    response_model=ResponseEnvelope,
    summary="Menghapus Program",
    description="Menghapus program berdasarkan ID."
)
async def delete_program(
    program_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        error_response = ResponseEnvelope(
            status="error",
            message="ID program tidak valid. ID harus berupa 24 karakter hex string.",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )

    result = await db.programs.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        error_response = ResponseEnvelope(
            status="error",
            message="Program tidak ditemukan",
            data=None
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.model_dump()
        )

    return ResponseEnvelope(
        status="success",
        message="Program berhasil dihapus",
        data=None
    )
