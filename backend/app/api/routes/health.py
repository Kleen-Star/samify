from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
        database = "connected"
    except SQLAlchemyError:
        database = "unavailable"
    return {
        "success": database == "connected",
        "message": "OK" if database == "connected" else "Database unavailable",
        "data": {"api": "ok", "database": database},
    }
