from fastapi import APIRouter, Depends, HTTPException, status
from backend.models import UserCreate, UserResponse
from backend.database import user_collection
from backend.core.security import get_password_hash
from backend.dependencies import get_admin_user
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/hr", response_model=UserResponse)
async def create_hr(user: UserCreate, admin: dict = Depends(get_admin_user)):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hr_data = {
        "name": user.name,
        "email": user.email,
        "password": get_password_hash(user.password),
        "role": "hr"
    }
    
    new_user = await user_collection.insert_one(hr_data)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    # Convert _id to string for the response model
    created_user["_id"] = str(created_user["_id"])
    return created_user

@router.get("/hr", response_model=List[UserResponse])
async def list_hrs(admin: dict = Depends(get_admin_user)):
    hrs = await user_collection.find({"role": "hr"}).to_list(100)
    for hr in hrs:
        hr["_id"] = str(hr["_id"])
    return hrs

@router.delete("/hr/{hr_id}")
async def delete_hr(hr_id: str, admin: dict = Depends(get_admin_user)):
    delete_result = await user_collection.delete_one({"_id": ObjectId(hr_id), "role": "hr"})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="HR not found")
    return {"message": "HR deleted successfully"}
