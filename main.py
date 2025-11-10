from fastapi import FastAPI
from db.database import engine
from models import models
from routers import api_router
from core.config import settings

app = FastAPI(title="Todo Application", description="Todos Manager", version=settings.API_VERSION)

@app.get("/")
async def root():
    return {
        "App": settings.PROJECT_NAME,
        "Version": settings.API_VERSION,
        "health": "Healthy"
    }


models.Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix=settings.API_VERSION)

