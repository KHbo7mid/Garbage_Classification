from fastapi import FastAPI
from routes.health_check import health
from routes.classification import router
from helpers.Settings import get_settings
import uvicorn
app=FastAPI(
    title=get_settings.APP_NAME,
    version=get_settings.APP_VERSION,
    description="Garbage Classification API using YOLO and FastAPI",
    
)

app.include_router(health)
app.include_router(router)


