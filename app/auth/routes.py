from fastapi import APIRouter, HTTPException, Response
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
async def xero_callback(code: str, response: Response):
    '''
    Get the authorization code and exchange it for an access token
    '''
    if not code:
        raise HTTPException(
            status_code=400, detail="Authorization code is missing")
    print(f"\n----code:: {code}\n")
    access_token = get_access_token(code)
    if access_token:
        # Store token in HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # Prevent JS access
            secure=True,  # Ensure this is used only over HTTPS in production
            samesite="Strict",  # Protect against CSRF
            max_age=1800  # Token expiration (30 minutes)
        )
        return {"msg": "Login successful", "access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="No access token in response")

    # return {"access_token": access_token}
