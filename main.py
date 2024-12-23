from fastapi import FastAPI
from app.auth.routes import auth_router
import uvicorn

app = FastAPI()

# routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, ssl_keyfile="./certs/key.pem", ssl_certfile="./certs/cert.pem")
