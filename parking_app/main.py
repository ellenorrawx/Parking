from fastapi import FastAPI
from parking_app.db.db import Base, engine

from parking_app.api import user, parking, booking

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Parking System")

app.include_router(user.router)
app.include_router(parking.router)
app.include_router(booking.router)