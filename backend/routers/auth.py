from fastapi import APIRouter, HTTPException, Depends, status
from backend.models import LoginRequest, Token
from backend.database import user_collection
from backend.core.security import verify_password, create_access_token, get_password_hash
from bson import ObjectId

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    # Check for hardcoded admin first for convenience or check DB
    # The requirement says admin/admin@123
    
    user = await user_collection.find_one({"$or": [{"email": request.email}, {"name": request.email}]})
    
    if not user:
        # If no admin exists in DB, check if it's the default one and create it
        if request.email == "admin" and request.password == "admin@123":
            admin_data = {
                "name": "admin",
                "email": "admin@careerpulse.ai",
                "password": get_password_hash("admin@123"),
                "role": "admin"
            }
            new_user = await user_collection.insert_one(admin_data)
            user = await user_collection.find_one({"_id": new_user.inserted_id})
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(subject=str(user["_id"]))
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"],
        "name": user["name"]
    }
