from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import os

from db_orm.crud import get_puffins_history, get_puffins_status

app = FastAPI()

# Настраиваем CORS для GitHub Pages и локальной разработки
ALLOWED_ORIGINS = [
    "https://simonoffcc.github.io",  # GitHub Pages домен
    "http://localhost:8000",
    "http://localhost:3000",
]

if os.getenv("PRODUCTION_DOMAIN"):
    ALLOWED_ORIGINS.append(os.getenv("PRODUCTION_DOMAIN"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/puffins/history")
async def get_history(days: int = 14):
    """
    Get puffins availability history for the last N days
    """
    history = get_puffins_history(days)
    return [
        {
            "date": record.date.isoformat(),
            "is_puffins": record.is_puffins,
            "message": record.message
        }
        for record in history
    ]

@app.get("/api/puffins/today")
async def get_today():
    """
    Get today's puffins status
    """
    today = get_puffins_status(date.today())
    if today:
        return {
            "date": today.date.isoformat(),
            "is_puffins": today.is_puffins,
            "message": today.message
        }
    return {
        "date": date.today().isoformat(),
        "is_puffins": None,
        "message": "Нет данных на сегодня"
    } 