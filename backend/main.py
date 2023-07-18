from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3, json, datetime, os
from contextlib import contextmanager
from openai_handle import openai_chat

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

class MessageData(BaseModel):
    uuid: str
    dateTime: str
    text: str
    inversion: bool
    error: bool
    loading: bool

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

@app.post("/message")
async def receive_message(message_data: MessageData):

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM chats WHERE id=?", (message_data.uuid,))
    result = cursor.fetchone()

    if result:
        messages = json.loads(result[0])
        messages_list = []
        for mes in messages:
            if mes["inversion"]:
                messages_list.append({"role": "system", "content": mes["text"]})
            else:
                messages_list.append({"role": "user", "content": mes["text"]})
        messages_list.append({"role": "user", "content": message_data.text})
        response_text = openai_chat(messages_list)
        response_message = {
            "dateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": response_text,
            "inversion": False,
            "error": False,
            "loading": False,
        }
        messages.append({
            "dateTime": message_data.dateTime,
            "text": message_data.text,
            "inversion": message_data.inversion,
            "error": message_data.error,
            "loading": message_data.loading,
        })
        messages.append(response_message)
        cursor.execute("UPDATE chats SET messages=? WHERE id=?", (json.dumps(messages), message_data.uuid))
        conn.commit()
    else:
        raise HTTPException(status_code=400, detail="Chat not found")

    conn.close()
    return {"status": "success"}

@app.post("/clear/{chat_id}")
async def chat_id(chat_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET messages=? WHERE id=?", ('[]', chat_id))
    conn.commit()
    conn.close()
    return {"status": "success"}