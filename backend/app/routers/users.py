from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter()


@router.get("/")
def list_users(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    users = db.query(User).filter(User.is_active == True).all()
    return [{
        "id": str(u.id),
        "email": u.email,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "role": u.role,
    } for u in users]
