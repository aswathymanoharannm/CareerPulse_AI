from fastapi import APIRouter, Depends, Query
from backend.models import JobResponse
from backend.database import job_collection
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skill: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 50
):
    query = {}
    if skill:
        # Case-insensitive search for skill in the skills array
        query["skills"] = {"$regex": skill, "$options": "i"}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
        
    jobs = await job_collection.find(query).sort("posted_date", -1).to_list(limit)
    for job in jobs:
        job["_id"] = str(job["_id"])
    return jobs

@router.get("/stats")
async def get_job_stats():
    total_jobs = await job_collection.count_documents({})
    # This is a simple placeholder for analytics
    return {
        "total_jobs": total_jobs,
        "recent_trends": "High demand in Python and Data Science"
    }
