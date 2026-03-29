from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import FileResponse
import os
import json
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

MEMORY_FILE = "memory.json"

# загрузка памяти
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = []

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

class Msg(BaseModel):
    text: str

SYSTEM = """
Ты личный ИИ пользователя.
Ты выполняешь его задачи.
Ты отвечаешь чётко.
Ты помогаешь решать любые задачи.
"""

@app.get("/")
def home():
    return FileResponse("index.html")

# 🌐 интернет (простая версия)
def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        r = requests.get(url).json()
        return r.get("Abstract", "")[:500]
    except:
        return ""

@app.post("/chat")
def chat(msg: Msg):

    web_info = search_web(msg.text)

    memory.append({"role": "user", "content": msg.text})

    messages = [{"role": "system", "content": SYSTEM}]

    if web_info:
        messages.append({"role": "system", "content": f"Информация из интернета: {web_info}"})

    messages += memory[-10:]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    memory.append({"role": "assistant", "content": answer})
    save_memory()

    return {"answer": answer}

# 📂 загрузка файлов
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    memory.append({"role": "system", "content": f"Файл пользователя: {text[:2000]}"})
    save_memory()

    return {"status": "файл добавлен в память"}
