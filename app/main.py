from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from core.dependencies import get_supabase_client
from models.errors import *
from pydantic import BaseModel

app = FastAPI()

origins = [
    # TODO: Restrict to specific frontend domains
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/games", tags=["games"])

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
response_time = Histogram('http_request_duration_seconds', 'Response time in seconds')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    request_count.inc()
    with response_time.time():
        response = await call_next(request)
    return response

@app.get("/metrics")
def metrics():
    return generate_latest()

@app.get("/", responses={200: {"model": dict}})
async def read_root():
    return {"service": "games-service"}

@app.get("/health/liveness", responses={200: {"model": dict}})
async def liveness():
    return {"status": "alive"}

@app.get("/health/readiness", responses={
    200: {"model": dict},
    500: {"model": InternalServerError}
})
async def readiness():
    try:
        supabase = get_supabase_client()
        response = supabase.table("games").select("*").limit(1).execute()
        if response.data:
            return {"status": "ready"}
        else:
            return {"status": "not ready", "error": "no found games"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
