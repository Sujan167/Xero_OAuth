import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    XERO_CLIENT_ID = os.getenv("XERO_CLIENT_ID")
    XERO_CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
    XERO_REDIRECT_URI = os.getenv("XERO_REDIRECT_URI")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    TOKEN_EXPIRY_BUFFER = 300  # Buffer in seconds for token expiry
