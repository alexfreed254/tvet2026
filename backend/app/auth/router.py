from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, supabase
from app.models.user import User
from app.auth.schemas import LoginRequest, LoginResponse, RegisterRequest
from app.auth.dependencies import get_current_user, require_admin

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password,
        })
        if not auth_response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = db.query(User).filter(User.id == auth_response.user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User profile not found")

        return LoginResponse(
            access_token=auth_response.session.access_token,
            user_id=str(user.id),
            role=user.role,
            full_name=f"{user.first_name} {user.last_name}",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    try:
        auth_response = supabase.auth.admin.create_user({
            "email": data.email,
            "password": data.password,
            "email_confirm": True,
            "user_metadata": {
                "first_name": data.first_name,
                "last_name": data.last_name,
            },
        })
        user = User(
            id=auth_response.user.id,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            role=data.role,
            department_id=data.department_id,
            staff_number=data.staff_number,
            phone=data.phone,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered", "user_id": str(user.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "department_id": str(current_user.department_id) if current_user.department_id else None,
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    supabase.auth.sign_out()
    return {"message": "Logged out"}
