# main.py
import os
from fastapi import FastAPI, WebSocket, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from app.routes import chat, journal
from app.dependencies import get_openai_client

load_dotenv()

app = FastAPI()

# Include routers
app.include_router(chat.router)
app.include_router(journal.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Journaling API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await process_message(data)
            await websocket.send_text(response)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

async def process_message(message: str):
    # 여기에 메시지 처리 로직을 구현합니다.
    return f"Processed: {message}"
