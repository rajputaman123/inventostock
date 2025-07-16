from fastapi import FastAPI
from app.api import inventory
from app.db.database import create_db_and_tables
from app.db.redis_client import redis

app = FastAPI(title="Inventory Service API")

# Routers
app.include_router(inventory.router)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    await redis.initialize()

@app.on_event("shutdown")
async def on_shutdown():
    await redis.close()