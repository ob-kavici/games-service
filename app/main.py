from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from core.dependencies import get_supabase_client
from models.errors import *

app = FastAPI()

origins = [
    # TODO change the only allowed origin to the frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/games", tags=["games"])

@app.get("/")
async def read_root():
    return {"service": "games-service"}

@app.get("/health/liveness")
async def liveness():
    return {"status": "alive"}

@app.get("/health/readiness")
async def readiness():
    try:
        supabase = get_supabase_client()
        response = supabase.table("games").select("*").limit(1).execute()
        if response.status_code == 200:
            return {"status": "ready"}
        else:
            return {"status": "not ready", "error": response.error_message}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
