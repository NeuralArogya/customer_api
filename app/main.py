from fastapi import FastAPI
from app.router import router
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Customer API",
    description="A Customer API built with FastAPI and PostgreSQL",
    version="1.0.0"
)

# Include router
app.include_router(router, prefix="/customers", tags=["Customers"])

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Customer API is running!"}