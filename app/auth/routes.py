from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.auth.service import get_access_token, get_authorization_url

auth_router = APIRouter()


@auth_router.get("/login")
def xero_login():
    '''
    Redirect user to Xero's OAuth authorization page
    '''
    authorization_url = get_authorization_url()
    return RedirectResponse(url=authorization_url)


@auth_router.get("/callback")
async def xero_callback(code: str):
    '''
    Get the authorization code and exchange it for an access token
    '''
    if not code:
        raise HTTPException(
            status_code=400, detail="Authorization code is missing")
    print(f"\n----code:: {code}\n")
    access_token = get_access_token(code)

    return {"access_token": access_token}
