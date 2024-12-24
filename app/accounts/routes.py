from fastapi import APIRouter, HTTPException, Request, Depends
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.accounts.service import fetch_chart_of_accounts, get_tenant_id, create_accounts_service
from app.utils.logger import logger
accounts_router = APIRouter()

@accounts_router.get("/chart-of-accounts")
async def get_chart_of_accounts(request: Request, db: Session = Depends(get_db)):
    """
    Retrieve Chart of Accounts using the access token from cookies
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        logger.error("Token not found or expired")
        raise HTTPException(status_code=401, detail="Token not found or expired")

    try:
        tenant_id = await get_tenant_id(access_token)
        data = await fetch_chart_of_accounts(access_token, tenant_id)

        await create_accounts_service(data['Accounts'], db)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chart of accounts: {str(e)}")
