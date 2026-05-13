from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, admin, hr, jobs
import uvicorn

app = FastAPI(title="CareerPulse AI API")

@app.on_event("startup")
async def startup_db_client():
    from backend.database import check_db
    await check_db()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(hr.router, prefix="/hr", tags=["HR"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

@app.get("/")
async def root():
    return {"message": "Welcome to CareerPulse AI API"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
