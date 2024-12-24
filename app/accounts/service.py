from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Dict, List
from app.config import Config
from app.models.account_model import Account
import httpx
from app.utils.logger import logger

async def fetch_chart_of_accounts(access_token: str, tenant_id: str):
    '''
    Fetch Chart of Accounts from Xero
    '''
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Xero-Tenant-id": tenant_id
    }
    logger.info("Fetching Chart of Accounts")
    # Using httpx for asynchronous HTTP requests
    async with httpx.AsyncClient() as client:
        response = await client.get(Config.CHART_OF_ACCOUNTS_URL, headers=headers)

    if response.status_code != 200:
        logger.error("Failed to fetch Chart of Accounts")
        raise Exception("Failed to fetch Chart of Accounts", response.json())

    return response.json()


async def get_tenant_id(access_token: str):
    '''
    Fetch Tenant ID from Xero
    '''
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    logger.info("Fetching Tenant ID")
    # Use httpx to make an asynchronous GET request
    async with httpx.AsyncClient() as client:
        response = await client.get(Config.TENANT_ID_URL, headers=headers)

    if response.status_code != 200:
        logger.error("Failed to fetch Tenant ID")
        raise Exception("Failed to fetch Tenant ID", response.json())

    return response.json()[0]["tenantId"]


BATCH_SIZE = 50  # Set the batch size (you can adjust this value)


async def create_accounts_service(accounts_data: List[Dict], db: Session):
    logger.info("Creating accounts in the database")
    count = 0  # Counter to track the number of processed records in the current batch

    for account_data in accounts_data:
        # Parse the UpdatedDateUTC to a datetime object
        updated_date = Account.parse_updated_date(
            account_data['UpdatedDateUTC'])

        logger.info(f"Processing account: {account_data['Name']}")
        # Check if the account already exists based on AccountID (or another unique field)
        existing_account = db.query(Account).filter(
            Account.AccountID == account_data["AccountID"]).first()

        if existing_account:
            logger.info(f"Account {account_data['Name']} already exists")
            # Account already exists, skip insertion
            continue

        # Create a new Account instance
        db_account = Account(
            AccountID=account_data["AccountID"],
            Code=account_data["Code"],
            Name=account_data["Name"],
            Status=account_data["Status"],
            Type=account_data["Type"],
            TaxType=account_data["TaxType"],
            Description=account_data["Description"],
            Class=account_data["Class"],
            SystemAccount=account_data["SystemAccount"],
            EnablePaymentsToAccount=account_data["EnablePaymentsToAccount"],
            ShowInExpenseClaims=account_data["ShowInExpenseClaims"],
            BankAccountType=account_data["BankAccountType"],
            ReportingCode=account_data["ReportingCode"],
            ReportingCodeName=account_data["ReportingCodeName"],
            HasAttachments=account_data["HasAttachments"],
            UpdatedDateUTC=updated_date,
            AddToWatchlist=account_data["AddToWatchlist"]
        )

        try:
            # Add the new account to the session
            db.add(db_account)
            count += 1

            # Commit in batches
            if count >= BATCH_SIZE:
                logger.info(f"Committing batch of {count} accounts")
                db.commit()
                count = 0  # Reset counter after commit

        except Exception as e:
            db.rollback()  # Rollback the transaction
            logger.error(f"Unexpected error occurred: {e}")  # Log the error
            continue  # Skip this account and proceed to the next one

    # Commit any remaining accounts if they haven't been committed yet
    if count > 0:
        logger.info(f"Committing remaining {count} accounts")
        db.commit()

    return True
