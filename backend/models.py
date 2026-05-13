from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str # admin, hr, student

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    skills: List[str]
    link: str
    salary: Optional[str] = "Not Specified"
    posted_date: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: str = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    skills: List[str] = []
    github_url: Optional[str] = None

class StudentResponse(StudentCreate):
    id: str = Field(alias="_id")
    added_by: str # HR ID
    model_config = ConfigDict(populate_by_name=True)
