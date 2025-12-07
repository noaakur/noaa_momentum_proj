from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import auth

# Import models so they're registered with Base
from app import models  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Team Presence Dashboard",
    description="API for managing team member availability statuses",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - allows frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

