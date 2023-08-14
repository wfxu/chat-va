from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3, json, datetime, os
from contextlib import contextmanager
from openai_handle import openai_chat

app = FastAPI()
router = APIRouter()

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
    u_id: str
    dateTime: str
    text: str
    is_user: int
    error: int
    loading: int

class MessageText(BaseModel):
    text: str

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/login")
async def login(login_data: LoginData):
    if login_data.username == "admin" and login_data.password == "password":
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@router.get("/chat")
async def chat():
    # 一列表形式返回 chats ids
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT u_id FROM users")
    result = cursor.fetchall()
    conn.close()
    return [i[0] for i in result]

@router.get("/chat/add")
async def add_item():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(u_id) FROM users")
    max_id = cursor.fetchone()[0]
    if max_id is not None:
        new_id = max_id + 1
    else:
        new_id = 1
    cursor.execute("insert into users (u_id) values (?)", (new_id,))
    conn.commit()
    return {"u_id": new_id}

@router.get("/chat/{chat_id}")
async def chat_id(chat_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT m_id, datetime, content, is_user, error, loading FROM messages WHERE u_id=? order by m_id", (chat_id,))
    results = cursor.fetchall()

    if results:
        messages = []
        for result in results:
            data = {
                "m_id": result[0],
                "datetime": result[1],
                "text": result[2],
                "is_user": result[3],
                "error": result[4],
                "loading": result[5]
            }
            messages.append(data)
        response = {"chat_id": chat_id, "messages": messages}
    else:
        response = {"detail": "Chat not found"}
    conn.close()
    return response

@router.post("/chat/message")
async def receive_message(message_data: MessageData):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(m_id) FROM messages where u_id=?", (message_data.u_id,))
    max_m_id = cursor.fetchone()[0]
    if max_m_id is not None:
        new_m_id = max_m_id + 1
    else:
        new_m_id = 1
    cursor.execute("INSERT INTO messages (u_id, m_id, dateTime, content, is_user, error, loading) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (message_data.u_id, new_m_id, message_data.dateTime, message_data.text, message_data.is_user, message_data.error, message_data.loading))
    conn.commit()
    cursor.execute("SELECT m_id, datetime, content, is_user, error, loading FROM messages WHERE u_id=? order by m_id", (message_data.u_id,))
    results = cursor.fetchall()

    if results:
        messages = []
        messages_list = []
        for result in results:
            data = {
                "u_id":message_data.u_id,
                "m_id": result[0],
                "datetime": result[1],
                "text": result[2],
                "is_user": result[3],
                "error": result[4],
                "loading": result[5]
            }
            messages.append(data)
            if not result[3]:
                role = "system"
            else:
                role = "user"
            messages_list.append({"role": role, "content": result[2]})
        messages.append({
            "u_id": message_data.u_id,
            "m_id": new_m_id,
            "dateTime": message_data.dateTime,
            "text": message_data.text,
            "is_user": message_data.is_user,
            "error": message_data.error,
            "loading": message_data.loading,
        })
        messages_list.append({"role": "user", "content": message_data.text})
        response_text = openai_chat(messages_list)
        response_message = {
            "u_id": message_data.u_id,
            "m_id": new_m_id + 1,
            "dateTime": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "text": response_text,
            "is_user": 0,
            "error": 0,
            "loading": 0,
        }
        messages.append(response_message)
        cursor.execute("INSERT INTO messages (u_id, m_id, dateTime, content, is_user, error, loading) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (message_data.u_id, response_message["m_id"], response_message["dateTime"], response_message["text"], 0, response_message["error"], response_message["loading"]))
        conn.commit()
    else:
        raise HTTPException(status_code=400, detail="Chat not found")

    conn.close()
    return {"status": "success"}

@router.post("/chat/clear/{chat_id}")
async def clear_chart(chat_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("delete from messages WHERE u_id=?", (chat_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

@router.post("/chat/delete/{chat_id}")
async def delete_chart(chat_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("delete from messages WHERE u_id=?", (chat_id,))
    cursor.execute("delete from users WHERE u_id=?", (chat_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

@router.post("/chat/{chat_id}/delete/{conv_id}")
async def delete_chart_conv(chat_id: int, conv_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("delete from messages WHERE u_id=? and m_id=?", (chat_id,conv_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@router.post("/chat/{chat_id}/update/{conv_id}")
async def update_chat_conv(chat_id: int, conv_id: int, message: MessageText):
    text = message.text
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("update messages set content=? where u_id=? and m_id=?", (text, chat_id, conv_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@router.post("/chat/{chat_id}/generate/{conv_id}")
async def generate_chat_conv(chat_id: int, conv_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT m_id, datetime, content, is_user, error, loading FROM messages WHERE u_id=? and m_id < ? order by m_id", (chat_id, conv_id))
    results = cursor.fetchall()

    if results:
        messages_list = []
        for result in results:
            if not result[3]:
                role = "system"
            else:
                role = "user"
            messages_list.append({"role": role, "content": result[2]})
        response_text = openai_chat(messages_list)
        cursor.execute("update messages set content=? where u_id=? and m_id=?", (response_text, chat_id, conv_id))
        conn.commit()
    else:
        raise HTTPException(status_code=400, detail="Chat not found")

    conn.close()
    return {"status": "success"}

app.include_router(router, prefix="/api")