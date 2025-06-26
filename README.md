# FastAPI Image Upload Server (Render)

Este servidor recibe imágenes JPEG por HTTP POST y las expone en una ruta pública para visualización en aplicaciones como detección de manos con MediaPipe.

## Endpoints

- `POST /upload` → Sube una imagen (`multipart/form-data`) como `file`
- `GET /latest.jpg` → Retorna la imagen más reciente
- `GET /static/latest.jpg` → Alias directo

## Despliegue

1. Sube este repositorio a GitHub
2. Conéctalo en [https://render.com](https://render.com)
3. Crea un nuevo servicio tipo **Web Service**
4. Usa el siguiente comando para iniciar:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
