from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

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
    return {"service": "games-service", "status": "running"}