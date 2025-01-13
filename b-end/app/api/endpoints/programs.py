from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Query
from app.models.schemas import ProgramBase, ProgramResponse
from app.core.database import get_database
from app.api.deps import get_current_active_user
from app.utils.file_handler import save_upload_file
from typing import List, Literal, Union, Optional
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from enum import Enum

class ProgramType(str, Enum):
    ALL = "all"
    HUMAN_LIBRARY = "human_library"
    WORKSHOP = "workshop"
    SOSIALISASI = "sosialisasi"

router = APIRouter(tags=["programs"])

@router.post(
    "", 
    response_model=ProgramResponse,
    summary="Membuat Program Baru",
    description="""
    Membuat program baru dengan gambar.
    
    **Format Gambar yang Didukung:**
    - JPG/JPEG
    - PNG
    - GIF
    
    **Batasan:**
    - Ukuran maksimal file: 5MB
    
    **Tipe Program yang Tersedia:**
    - human_library: Program Human Library
    - workshop: Program Workshop
    - sosialisasi: Program Sosialisasi
    """
)
async def create_program(
    title: str = Form(..., description="Judul program", example="Workshop Pemulihan Mental"),
    description: str = Form(..., description="Deskripsi program", example="Workshop untuk pemulihan kesehatan mental..."),
    program_type: ProgramType = Form(
        ..., 
        description="Tipe program (human_library, workshop, sosialisasi)",
        exclude=["ALL"]
    ),
    image: UploadFile = File(
        ..., 
        description="File gambar untuk program (JPG, PNG, GIF, max 5MB)",
        media_type="image/*"
    ),
    start_date: datetime = Form(..., description="Tanggal mulai program", example="2024-01-01T00:00:00"),
    end_date: datetime = Form(..., description="Tanggal selesai program", example="2024-01-02T00:00:00"),
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Upload gambar
    image_url = await save_upload_file(image)
    
    program_data = {
        "title": title,
        "description": description,
        "program_type": program_type.value,
        "image": image_url,
        "start_date": start_date,
        "end_date": end_date,
        "created_at": datetime.utcnow(),
        "author": current_user["email"]
    }
    
    # Validate program data using ProgramBase
    program = ProgramBase(**program_data)
    
    result = await db.programs.insert_one(program.model_dump())
    created_program = await db.programs.find_one({"_id": result.inserted_id})
    return created_program

@router.get(
    "", 
    response_model=List[ProgramResponse],
    summary="Mengambil Semua Program",
    description="""
    Mengambil daftar program yang tersedia.
    
    **Filter Tipe Program:**
    - all: Menampilkan semua program
    - human_library: Hanya program human library
    - workshop: Hanya program workshop
    - sosialisasi: Hanya program sosialisasi
    """
)
async def get_programs(
    program_type: ProgramType = Query(
        ProgramType.ALL,
        description="Filter berdasarkan tipe program"
    ),
    db=Depends(get_database)
):
    query = {}
    if program_type != ProgramType.ALL:
        query["program_type"] = program_type.value
        
    programs = await db.programs.find(query).to_list(1000)
    return programs

@router.get(
    "/{program_id}", 
    response_model=ProgramResponse,
    summary="Mengambil Detail Program",
    description="Mengambil detail program berdasarkan ID."
)
async def get_program(program_id: str, db=Depends(get_database)):
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="ID program tidak valid. ID harus berupa 24 karakter hex string."
        )
    
    program = await db.programs.find_one({"_id": object_id})
    if not program:
        raise HTTPException(
            status_code=404,
            detail="Program tidak ditemukan"
        )
    return program

@router.delete(
    "/{program_id}",
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
        raise HTTPException(
            status_code=400,
            detail="ID program tidak valid. ID harus berupa 24 karakter hex string."
        )
    
    result = await db.programs.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Program tidak ditemukan"
        )
    return {"message": "Program berhasil dihapus"}
