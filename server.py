from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import FileResponse
import os, json, base64

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

MEMORY_FILE = "memory.json"
PROFILE_FILE = "profile.json"
TASKS_FILE = "tasks.json"

def load(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

memory = load(MEMORY_FILE, [])
profile = load(PROFILE_FILE, {})
tasks = load(TASKS_FILE, [])

class Msg(BaseModel):
    text: str

SYSTEM = """
Ты личный ИИ пользователя.

Правила:
- Ты помогаешь во всех задачах
- Ты адаптируешься под пользователя
- Ты запоминаешь важную информацию
- Ты отвечаешь чётко и понятно
"""

@app.get("/")
def home():
    return FileResponse("index.html")

def extract_memory(text):
    keywords = ["меня зовут", "я хочу", "мне важно", "запомни"]
    for k in keywords:
        if k in text.lower():
            return text
    return None

@app.post("/chat")
def chat(msg: Msg):
    global memory, profile

    important = extract_memory(msg.text)
    if important:
        profile["info"] = profile.get("info", []) + [important]
        save(PROFILE_FILE, profile)

    memory.append({"role": "user", "content": msg.text})

    messages = [{"role": "system", "content": SYSTEM}]

    if "info" in profile:
        messages.append({
            "role": "system",
            "content": f"Информация о пользователе: {profile['info']}"
        })

    messages += memory[-10:]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    memory.append({"role": "assistant", "content": answer})
    save(MEMORY_FILE, memory)

    return {"answer": answer}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()

    if file.content_type.startswith("image/"):
        b64 = base64.b64encode(content).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Опиши изображение"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{file.content_type};base64,{b64}"
                            },
                        },
                    ],
                }
            ],
        )

        return {"status": response.choices[0].message.content}

    text = content.decode("utf-8", errors="ignore")
    memory.append({"role": "system", "content": text[:1000]})
    save(MEMORY_FILE, memory)

    return {"status": "файл сохранён"}
