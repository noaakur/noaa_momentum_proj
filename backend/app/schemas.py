from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class StatusEnum(int, Enum):
    """Allowed status values."""
    WORKING = 0
    WORKING_REMOTELY = 1
    ON_VACATION = 2
    BUSINESS_TRIP = 3


# Mapping for display names
STATUS_LABELS = {
    StatusEnum.WORKING: "Working",
    StatusEnum.WORKING_REMOTELY: "Working Remotely",
    StatusEnum.ON_VACATION: "On Vacation",
    StatusEnum.BUSINESS_TRIP: "Business Trip",
}


# --- Auth Schemas ---

class LoginRequest(BaseModel):
    """Request body for login endpoint."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Response from login endpoint."""
    access_token: str
    token_type: str = "bearer"


# --- User Schemas ---

class UserResponse(BaseModel):
    """User data returned in API responses."""
    id: int
    full_name: str
    status: str
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows creating from SQLAlchemy model


class StatusUpdateRequest(BaseModel):
    """Request body for updating user status."""
    status: StatusEnum

