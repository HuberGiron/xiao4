from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hubergiron.mx"],  # o ["*"] para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile):
    with open("static/latest.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "ok"}

@app.get("/latest.jpg")
def get_image():
    return FileResponse("static/latest.jpg")

@app.websocket("/ws")  # (Opcional si algún cliente desea usar WebSocket)
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            with open("static/latest.jpg", "wb") as f:
                f.write(data)
    except Exception as e:
        print("WebSocket closed:", e)
    finally:
        await websocket.close()

app.mount("/static", StaticFiles(directory="static"), name="static")
