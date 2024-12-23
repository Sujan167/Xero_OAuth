import requests
from app.config import Config


async def fetch_chart_of_accounts(access_token: str, tenant_id: str):
    '''
    Fetch Chart of Accounts from Xero
    '''
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Xero-Tenant-id": tenant_id
    }
    response = requests.get(Config.CHART_OF_ACCOUNTS_URL, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch Chart of Accounts", response.json())

    return response.json()


async def get_tenant_id(access_token: str):
    '''
    Fetch Tenant ID from Xero
    '''
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(Config.TENANT_ID_URL, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch Tenant ID", response.json())
    return response.json()[0]["tenantId"]
