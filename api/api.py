from fastapi import FastAPI
from fastapi import WebSocket

app = FastAPI()


@app.get("/hello")
def hello() -> dict:
    return {"message": "Hello World"}

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