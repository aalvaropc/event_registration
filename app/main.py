from fastapi import FastAPI
from app.api.v1.endpoints import registration
from app.db.init_db import init_db
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(registration.router, prefix="/v1/registration")

@app.on_event("startup")
async def on_startup():
    await init_db(engine)

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)