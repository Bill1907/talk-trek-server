import os
from fastapi import FastAPI
from fastapi import WebSocket
from dotenv import load_dotenv
from openai import OpenAI

app = FastAPI()

load_dotenv()
key = os.environ.get("OPEN_API_KEY")

@app.get("/")
def hello() -> dict:
    client = OpenAI(api_key=key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    return {"message": completion.choices[0].message.content
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Websocket connection')
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print('Error:', e)
    finally:
        await websocket.close()