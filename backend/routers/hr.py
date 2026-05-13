from fastapi import APIRouter, Depends, HTTPException, status
from backend.models import StudentCreate, StudentResponse
from backend.database import student_collection, user_collection
from backend.dependencies import get_hr_user
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/students", response_model=StudentResponse)
async def add_student(student: StudentCreate, hr: dict = Depends(get_hr_user)):
    existing_student = await student_collection.find_one({"email": student.email})
    if existing_student:
        raise HTTPException(status_code=400, detail="Student email already exists")
    
    student_data = student.model_dump()
    student_data["added_by"] = str(hr["_id"])
    
    new_student = await student_collection.insert_one(student_data)
    created_student = await student_collection.find_one({"_id": new_student.inserted_id})
    created_student["_id"] = str(created_student["_id"])
    return created_student

@router.get("/students", response_model=List[StudentResponse])
async def list_students(hr: dict = Depends(get_hr_user)):
    # HR can see all students or just the ones they added? 
    # Usually HR/Admin can see all.
    query = {}
    if hr["role"] == "hr":
        query = {"added_by": str(hr["_id"])}
        
    students = await student_collection.find(query).to_list(100)
    for student in students:
        student["_id"] = str(student["_id"])
    return students

@router.delete("/students/{student_id}")
async def delete_student(student_id: str, hr: dict = Depends(get_hr_user)):
    query = {"_id": ObjectId(student_id)}
    if hr["role"] == "hr":
        query["added_by"] = str(hr["_id"])
        
    delete_result = await student_collection.delete_one(query)
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found or not authorized")
    return {"message": "Student deleted successfully"}
