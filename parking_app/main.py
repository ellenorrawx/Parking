import sys
from pathlib import Path

# Добавляем корень проекта в путь, чтобы можно было импортировать parking_app
ROOT_DIR = Path(__file__).parent.parent  # это папка "Parking"
sys.path.append(str(ROOT_DIR))
from fastapi import FastAPI
from .db.db import Base, engine
from .api import user, parking, booking


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Parking System")

app.include_router(user.router)
app.include_router(parking.router)
app.include_router(booking.router)
