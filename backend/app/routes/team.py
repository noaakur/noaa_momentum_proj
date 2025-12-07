from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserResponse, StatusUpdateRequest, StatusEnum, STATUS_LABELS
from app.auth import get_current_user

router = APIRouter(tags=["team"])


@router.get("/team", response_model=List[UserResponse])
def get_team(
    status: Optional[List[StatusEnum]] = Query(default=None, description="Filter by status(es)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all team members with their statuses.
    Optionally filter by one or more statuses.
    
    Protected route - requires authentication.
    """
    query = db.query(User)
    
    # Apply status filter if provided
    if status:
        status_values = [s.value for s in status]
        query = query.filter(User.status.in_(status_values))
    
    users = query.order_by(User.full_name).all()
    
    # Convert to response format with status labels
    return [
        UserResponse(
            id=user.id,
            full_name=user.full_name,
            status=STATUS_LABELS[StatusEnum(user.status)],
            updated_at=user.updated_at
        )
        for user in users
    ]


@router.patch("/me/status", response_model=UserResponse)
def update_my_status(
    request: StatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the current user's availability status.
    
    Protected route - requires authentication.
    """
    # Update user's status
    current_user.status = request.status.value
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        status=STATUS_LABELS[StatusEnum(current_user.status)],
        updated_at=current_user.updated_at
    )

