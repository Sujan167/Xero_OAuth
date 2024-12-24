from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import RedirectResponse
from app.auth.service import get_access_token, get_authorization_url, refresh_access_token
from app.utils.logger import logger
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
        logger.error("Authorization code is missing")
        raise HTTPException(status_code=400, detail="Authorization code is missing")
    token = await get_access_token(code)
    if token:
        logger.info("Login successful")
        logger.info("Setting access token in cookies")
        # Store token in HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=token["access_token"],
            httponly=True,  # Prevent JS access
            secure=True,  # Ensure this is used only over HTTPS in production
            samesite="Strict",  # Protect against CSRF
            max_age=token['expires_in']  # Token expiration (30 minutes)
        )
        response.set_cookie(
            key="refresh_token",
            value=token["refresh_token"],
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=604800  # Token expiration (7 days)
        )
        return {"msg": "Login successful", "token": token}
    else:
        logger.error("No access token in response")
        raise HTTPException(status_code=400, detail="No access token in response")


@auth_router.get("/refresh")
async def refresh_token(request: Request, response: Response):
    """
    Refresh the access token using the refresh token stored in the cookies
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        logger.error("Refresh token missing")        
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        new_access_token, expires_in = refresh_access_token(refresh_token)
        # Update the access token cookie
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=expires_in
        )
        logger.info("Token refreshed")
        return {"msg": "Token refreshed", "access_token": new_access_token}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
