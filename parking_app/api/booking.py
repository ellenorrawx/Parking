from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from parking_app.db.db import get_db
from parking_app.db import models, schema

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/")
def book(data: schema.BookingCreate, db: Session = Depends(get_db)):

    parking = db.query(models.Parking).filter_by(id=data.parking_id).first()

    if parking.status != "free":
        return {"error": "not available"}

    parking.status = "reserved"

    booking = models.Booking(**data.dict())
    db.add(booking)

    db.commit()

    return {"message": "booked"}