import sqlite3
import json

with open("sample_data.json", encoding="utf-8") as f:
    data = json.load(f)

conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

# 创建表
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY,
        messages TEXT NOT NULL
    )
    """
)

# 将JSON数据导入表中
for item in data:
    cursor.execute(
        """
        INSERT INTO chats (id, messages)
        VALUES (?, ?)
        """,
        (item["id"], json.dumps(item["messages"])),
    )

conn.commit()
conn.close()
