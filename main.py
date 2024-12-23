from fastapi import FastAPI
from app.auth.routes import auth_router
from app.accounts.routes import accounts_router
import uvicorn

app = FastAPI()

# routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(accounts_router, prefix="/account", tags=["accounts"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, ssl_keyfile="./certs/key.pem", ssl_certfile="./certs/cert.pem")
