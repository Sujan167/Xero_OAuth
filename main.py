import os
import uvicorn
from fastapi import FastAPI
from app.utils.logger import logger
from app.auth.routes import auth_router
from app.accounts.routes import accounts_router

app = FastAPI()

# routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(accounts_router, prefix="/account", tags=["accounts"])

ENV = os.getenv("ENVIRONMENT") if os.getenv("ENVIRONMENT") else "PROD"
logger.info("Starting the application")
logger.info(f"--Environment: {ENV}--")

if ENV == "DEV" and __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, ssl_keyfile="./certs/key.pem", ssl_certfile="./certs/cert.pem")
