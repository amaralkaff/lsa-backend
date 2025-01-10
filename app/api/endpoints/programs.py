from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ProgramBase, ProgramResponse
from app.core.database import get_database
from app.api.deps import get_current_active_user
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("", response_model=ProgramResponse)
async def create_program(
    program: ProgramBase,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    program_dict = program.model_dump()
    result = await db.programs.insert_one(program_dict)
    created_program = await db.programs.find_one({"_id": result.inserted_id})
    return created_program

@router.get("", response_model=List[ProgramResponse])
async def get_programs(db=Depends(get_database)):
    programs = await db.programs.find().to_list(1000)
    return programs

@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: str, db=Depends(get_database)):
    from bson import ObjectId
    program = await db.programs.find_one({"_id": ObjectId(program_id)})
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.delete("/{program_id}")
async def delete_program(
    program_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    from bson import ObjectId
    result = await db.programs.delete_one({"_id": ObjectId(program_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"message": "Program deleted successfully"}
