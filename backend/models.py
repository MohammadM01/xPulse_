from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from backend.database import Base

class InvoiceStatus(str, enum.Enum):
    PENDING_TRIBUNAL = "pending_tribunal"
    APPROVED = "approved"
    REJECTED = "rejected"
    MINTING = "minting"
    MINTED = "minted"
    MINT_FAILED = "mint_failed"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, index=True) # Zoho Invoice ID
    amount = Column(Float, nullable=False)
    payer_name = Column(String, nullable=False)
    status = Column(String, default=InvoiceStatus.PENDING_TRIBUNAL) # Storing Enum as String for simplicity
    proof_tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    votes = relationship("Vote", back_populates="invoice")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    approver_id = Column(String, nullable=False) # Cliq User ID
    vote_type = Column(String, nullable=False) # "approve" or "flag"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    invoice = relationship("Invoice", back_populates="votes")

    __table_args__ = (
        UniqueConstraint('invoice_id', 'approver_id', name='uq_vote_invoice_approver'),
        Index('idx_votes_invoice', 'invoice_id'),
    )

class ZohoEvent(Base):
    __tablename__ = "zoho_events"

    id = Column(Integer, primary_key=True, index=True)
    zoho_event_id = Column(String, unique=True, index=True, nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())

class UserWallet(Base):
    __tablename__ = "user_wallets"

    user_id = Column(String, primary_key=True, index=True) # Cliq User ID
    wallet_address = Column(String, nullable=False)
