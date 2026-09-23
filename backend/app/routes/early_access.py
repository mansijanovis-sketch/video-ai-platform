from datetime import datetime, timezone
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import EarlyAccessSignup


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Early Access"],
)


class EarlyAccessRequest(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Name is required.")
        if not 2 <= len(normalized) <= 100:
            raise ValueError("Name must be between 2 and 100 characters.")
        return normalized

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class EarlyAccessResponse(BaseModel):
    success: bool
    message: str


@router.post("/early-access", response_model=EarlyAccessResponse)
def register_early_access(
    payload: EarlyAccessRequest,
    db: Session = Depends(get_db),
):
    normalized_email = payload.email.lower().strip()

    existing = (
        db.query(EarlyAccessSignup)
        .filter(EarlyAccessSignup.email == normalized_email)
        .first()
    )

    if existing:
        return EarlyAccessResponse(
            success=True,
            message="This email is already registered for early access.",
        )

    signup = EarlyAccessSignup(
        name=payload.name.strip(),
        email=normalized_email,
        created_at=datetime.now(timezone.utc),
    )

    try:
        db.add(signup)
        db.commit()
        db.refresh(signup)
    except Exception:
        db.rollback()
        logger.exception("Unable to persist early access registration")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register early access request.",
        )

    return EarlyAccessResponse(
        success=True,
        message="Early access registration received.",
    )
