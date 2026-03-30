from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI

app = FastAPI()
client = OpenAI()

class Msg(BaseModel):
    text: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(msg: Msg):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": msg.text}
            ]
        )

        answer = response.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        return {"answer": "Ошибка: " + str(e)}
