from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from db_orm.crud import get_puffins_history, get_puffins_status

app = FastAPI()

# Настраиваем CORS для GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://simonoffcc.github.io",  # Ваш GitHub Pages домен
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
    ],
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