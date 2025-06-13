import asyncio
from datetime import datetime
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from typing import List

from db_orm.database import Session
from db_orm.crud import get_puffins_history_last_two_weeks

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

app = FastAPI()

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
templates = Jinja2Templates(directory="webapp/templates")

@app.get("/")
async def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/puffins-data")
async def puffins_data():
    with Session() as session:
        history = get_puffins_history_last_two_weeks(session)
        return [{"date": record.date.strftime("%Y-%m-%d"), "is_available": record.is_puffins} for record in history]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Просто держим соединение открытым
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Это нужно, чтобы другие части приложения могли импортировать manager
__all__ = ["app", "manager"] 