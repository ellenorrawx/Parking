from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from .db import Base


# 👤 ROLES
class Role:
    ADMIN = "admin"
    USER = "user"


# 🅿️ PARKING STATUS
class ParkingStatus:
    FREE = "free"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


# 👤 USER
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default=Role.USER)


# 🅿️ PARKING
class Parking(Base):
    __tablename__ = "parkings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String, default=ParkingStatus.FREE)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)


# 📅 BOOKING
class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    parking_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="active")