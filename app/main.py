from fastapi import FastAPI
from app.routes import router
from loguru import logger

logger.info("InsightEngine started successfully")

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "InsightEngine is running"}