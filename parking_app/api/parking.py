from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from parking_app.db.db import get_db
from parking_app.db import models,schema

router = APIRouter(prefix="/parking", tags=["Parking"])


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Parking).all()


@router.post("/")
def create(parking: schema.ParkingCreate, db: Session = Depends(get_db)):
    new = models.Parking(**parking.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

router = APIRouter(prefix="/parking", tags=["Parking"])


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Parking).all()


@router.post("/")
def create(parking: schema.ParkingCreate, db: Session = Depends(get_db)):
    new = models.Parking(**parking.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new