from fastapi import APIRouter, HTTPException, Request
from app.accounts.service import fetch_chart_of_accounts
from app.accounts.service import get_tenant_id

accounts_router = APIRouter()


@accounts_router.get("/chart-of-accounts")
async def get_chart_of_accounts(request: Request):
    """
    Retrieve Chart of Accounts using the access token from cookies
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401, detail="Token not found or expired")

    try:
        tenant_id = await get_tenant_id(access_token)
        accounts = await fetch_chart_of_accounts(access_token, tenant_id)
        return {"data": accounts}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching chart of accounts: {str(e)}")
