from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI()  # ключ берётся автоматически из Environment

class Msg(BaseModel):
    text: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(msg: Msg):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=msg.text
        )

        return {"answer": response.output_text}

    except Exception as e:
        return {"answer": "Ошибка: " + str(e)}
