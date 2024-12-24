from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import re
from app.database.session import engine

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'

    AccountID = Column(String, primary_key=True, index=True)
    Code = Column(String, index=True)
    Name = Column(String)
    Status = Column(String)
    Type = Column(String)
    TaxType = Column(String)
    Description = Column(String)
    Class = Column(String)
    SystemAccount = Column(String, nullable=True)
    EnablePaymentsToAccount = Column(Boolean, default=False)
    ShowInExpenseClaims = Column(Boolean, default=False)
    BankAccountType = Column(String, nullable=True)
    ReportingCode = Column(String)
    ReportingCodeName = Column(String)
    HasAttachments = Column(Boolean, default=False)
    UpdatedDateUTC = Column(DateTime)
    AddToWatchlist = Column(Boolean, default=False)

    @staticmethod
    def parse_updated_date(updated_date: str) -> datetime:
        """
        Parse the Xero API's custom date format "/Date(1735020615208+0000)/"
        into a Python datetime object.
        """
        match = re.match(r"/Date\((\d+)(?:\+|\-)\d{4}\)/", updated_date)
        if match:
            timestamp = int(match.group(1))
            return datetime.utcfromtimestamp(timestamp / 1000)
        return None


Base.metadata.create_all(bind=engine)
