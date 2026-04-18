from pydantic import BaseModel
from typing import Literal


# 👤 USER
class UserCreate(BaseModel):
    username: str
    password: str
    role: Literal["admin", "user"]


# 🅿️ PARKING
class ParkingCreate(BaseModel):
    status: Literal["free", "occupied", "reserved"]
    latitude: float
    longitude: float


# 📅 BOOKING
class BookingCreate(BaseModel):
    user_id: int
    parking_id: int