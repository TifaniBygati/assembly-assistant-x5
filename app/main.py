from fastapi import FastAPI

from app.routers.clients import router as clients_router


app = FastAPI()

app.include_router(clients_router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

