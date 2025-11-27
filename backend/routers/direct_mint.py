from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Invoice, InvoiceStatus, ZohoEvent
from backend.schemas import DirectMintRequest
from backend.config import get_settings
from backend.worker import mint_proof_task
from redis import Redis
from rq import Queue, Retry

router = APIRouter()
settings = get_settings()

# Redis connection for enqueuing
q = None
if not settings.SYNC_TASKS:
    redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    q = Queue(connection=redis_conn)

@router.post("/direct-mint")
async def direct_mint(payload: DirectMintRequest, db: Session = Depends(get_db)):
    """
    Manually trigger minting for an invoice (Bypass Approval).
    """
    invoice_id = payload.invoice_id
    amount = payload.amount
    payer_name = payload.payer_name

    # 1. Idempotency Check
    event_id = f"direct_mint_{invoice_id}"
    if db.query(ZohoEvent).filter(ZohoEvent.zoho_event_id == event_id).first():
        return {"status": "ignored", "reason": "already_processed"}
    
    db.add(ZohoEvent(zoho_event_id=event_id))

    # 2. Check/Create Invoice
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        invoice = Invoice(
            id=invoice_id,
            amount=amount,
            payer_name=payer_name,
            status=InvoiceStatus.MINTING # Skip PENDING_TRIBUNAL
        )
        db.add(invoice)
    else:
        # If exists, update status to MINTING regardless of current state
        invoice.status = InvoiceStatus.MINTING
    
    db.commit()

    # 3. Trigger Worker
    # For direct mint, we might not have "approvers", so we use a system identifier
    approvers = ["MANUAL_TRIGGER"]

    if settings.SYNC_TASKS:
        print(f"Running Direct Mint task synchronously for {invoice_id}")
        mint_proof_task(invoice_id, approvers)
    else:
        q.enqueue(mint_proof_task, invoice_id, approvers, retry=Retry(max=3, interval=[10, 30, 60]))

    return {"status": "minting_started", "invoice_id": invoice_id}
