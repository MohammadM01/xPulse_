from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.models import InvoiceStatus

class VoteBase(BaseModel):
    approver_id: str
    vote_type: str

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    invoice_id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    id: str
    amount: float
    payer_name: str

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    status: str
    proof_tx_hash: Optional[str] = None
    created_at: datetime
    votes: List[Vote] = []

    class Config:
        from_attributes = True

class WebhookPayload(BaseModel):
    # Simplified payload structure from Zoho Books
    invoice_id: str
    amount: float
    customer_name: str

class CliqInteraction(BaseModel):
    # Structure for Cliq interaction payload
    action: str # "approve" or "flag"
    invoice_id: str
    user_id: str

class DirectMintRequest(BaseModel):
    invoice_id: str
    amount: float
    payer_name: str
