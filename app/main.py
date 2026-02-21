from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import router as chat_router
from pathlib import Path

app = FastAPI()

# API
app.include_router(chat_router)

# Static files
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve UI
@app.get("/")
def serve_ui():
    return FileResponse(STATIC_DIR / "index.html")
