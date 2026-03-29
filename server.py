from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import FileResponse
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

memory = []  # память

class Msg(BaseModel):
    text: str

SYSTEM = "Ты личный ИИ пользователя. Помогаешь во всём."

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(msg: Msg):

    memory.append({"role": "user", "content": msg.text})

    messages = [{"role": "system", "content": SYSTEM}] + memory[-10:]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    memory.append({"role": "assistant", "content": answer})

    return {"answer": answer}
