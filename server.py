from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Msg(BaseModel):
    text: str

SYSTEM = "Ты личный ИИ пользователя. Помогаешь во всём."

@app.post("/chat")
def chat(msg: Msg):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": msg.text}
        ]
    )
    return {"answer": response.choices[0].message.content}
