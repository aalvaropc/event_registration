from fastapi import FastAPI
from app.api.v1.endpoints import registration
from app.db.init_db import init_db
from app.db.session import engine

app = FastAPI()

app.include_router(registration.router, prefix="/v1/registration")

@app.on_event("startup")
async def on_startup():
    await init_db(engine)

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
