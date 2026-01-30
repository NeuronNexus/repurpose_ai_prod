import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.analyze import router as analyze_router
from app.api import report

# Load environment variables from .env file in backend root (development only)
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

app = FastAPI(title="RepurposeAI Backend")

# Configure CORS origins from environment variable `ALLOWED_ORIGINS`.
# Expected format: comma-separated list of origins (e.g. https://app.vercel.app,https://my-other)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(report.router)
app.include_router(analyze_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
