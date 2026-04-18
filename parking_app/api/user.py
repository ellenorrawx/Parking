from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from parking_app.db.db import get_db
from parking_app.db import models, schema

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register")
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter_by(
        username=username,
        password=password
    ).first()

    if not user:
        return {"error": "invalid credentials"}

    return {"message": "success", "role": user.role}