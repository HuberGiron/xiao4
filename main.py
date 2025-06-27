from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# ✅ Habilitar carpeta de imágenes
os.makedirs("static", exist_ok=True)

# ✅ Habilitar CORS para tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hubergiron.mx"],  # Cambia esto si necesitas otros orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Endpoint optimizado para subir imagen JPEG directa (sin multipart)
@app.post("/upload")
async def upload_image(request: Request):
    image_data = await request.body()
    with open("static/latest.jpg", "wb") as buffer:
        buffer.write(image_data)
    return {"status": "ok"}

# ✅ Servir la última imagen
@app.get("/latest.jpg")
def get_image():
    return FileResponse("static/latest.jpg", headers={"Cache-Control": "no-store"})

# ✅ WebSocket opcional
@app.websocket("/ws")
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

# ✅ Servir archivos estáticos (como /static/latest.jpg si lo deseas)
app.mount("/static", StaticFiles(directory="static"), name="static")
