from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="MakerFlow API",
    description="Backend MVP untuk AI-Powered Production Assistant",
    version="1.0.0"
)

# Konfigurasi CORS agar Next.js (frontend) bisa melakukan fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Saat produksi, ganti dengan URL frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from db.database import engine
from db import models  # noqa: F401
models.Base.metadata.create_all(bind=engine)

from api.routes import estimate, plans

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MakerFlow API is running!"}

app.include_router(estimate.router, tags=["Estimation"])
app.include_router(plans.router, tags=["Plans"])