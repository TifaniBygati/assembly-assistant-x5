from fastapi import FastAPI

from app.routers.clients import router as clients_router
from app.routers.health import router as health_router

app = FastAPI()
app.include_router(clients_router)
app.include_router(health_router)



