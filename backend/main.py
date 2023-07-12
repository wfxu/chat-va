from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import json
from contextlib import contextmanager

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginData(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
async def login(login_data: LoginData):
    if login_data.username == "admin" and login_data.password == "password":
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.get("/chat")
async def chat():
    # 一列表形式返回 chats ids
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chats")
    result = cursor.fetchall()
    conn.close()
    return [i[0] for i in result]

@app.get("/chat/{chat_id}")
async def chat_id(chat_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM chats WHERE id=?", (chat_id,))
    result = cursor.fetchone()

    if result:
        messages = json.loads(result[0])
        response = {"chat_id": chat_id, "messages": messages}
    else:
        response = {"detail": "Chat not found"}
    conn.close()
    return response