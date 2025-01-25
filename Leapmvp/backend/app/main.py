from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks, users, calendar
from app.services.nlp_service import NLPService
from app.services.ml_service import MLService

app = FastAPI(title="AI Task Scheduler")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI services
nlp_service = NLPService()
ml_service = MLService()

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])

@app.get("/")
async def root():
    return {"message": "AI Task Scheduler API"} 