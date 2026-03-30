from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

        answer = response.output[0].content[0].text

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Ошибка сервера: {str(e)}"}
