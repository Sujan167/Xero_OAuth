import httpx
from app.config import Config


def get_authorization_url():
    """
    Generate the Xero authorization URL
    """
    return (
        f"{Config.AUTHORIZATION_URL}?response_type=code&client_id={
            Config.CLIENT_ID}&"
        f"redirect_uri={Config.REDIRECT_URI}&scope={Config.SCOPE}&state=123"
    )


async def get_access_token(auth_code: str):
    """
    Exchange authorization code for access token (Asynchronous version)
    """
    token_payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": Config.REDIRECT_URI,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Use httpx for asynchronous HTTP requests
    async with httpx.AsyncClient() as client:
        response = await client.post(
            Config.TOKEN_URL, data=token_payload, headers=headers
        )

    if response.status_code != 200:
        raise Exception("Failed to fetch access token", response.json())

    token_data = response.json()
    return token_data


async def refresh_access_token(refresh_token: str):
    """
    Refresh the access token using the refresh token (Asynchronous version)
    """
    token_payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Use httpx for asynchronous HTTP requests
    async with httpx.AsyncClient() as client:
        response = await client.post(
            Config.TOKEN_URL, data=token_payload, headers=headers
        )

    if response.status_code != 200:
        raise Exception("Failed to refresh access token", response.json())

    token_data = response.json()
    return token_data["access_token"], token_data["expires_in"]
