import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLIENT_ID = os.getenv("XERO_CLIENT_ID")
    CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("XERO_REDIRECT_URI")
    SCOPE = os.getenv("XERO_SCOPE", "openid profile email accounting.transactions accounting.reports.read accounting.settings accounting.settings.read")
    AUTHORIZATION_URL = "https://login.xero.com/identity/connect/authorize"
    TOKEN_URL = "https://identity.xero.com/connect/token"
    CHART_OF_ACCOUNTS_URL = "https://api.xero.com/api.xro/2.0/Accounts"
    TENANT_ID_URL="https://api.xero.com/connections"
