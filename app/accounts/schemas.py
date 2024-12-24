from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    AccountID: str
    Code: str
    Name: str
    Status: str
    Type: str
    TaxType: str
    Description: str
    Class: str
    SystemAccount: Optional[str] = None
    EnablePaymentsToAccount: bool
    ShowInExpenseClaims: bool
    BankAccountType: Optional[str] = None
    ReportingCode: str
    ReportingCodeName: str
    HasAttachments: bool
    UpdatedDateUTC: datetime
    AddToWatchlist: bool

    class Config:
        orm_mode = True
