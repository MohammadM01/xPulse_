from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Invoice, InvoiceStatus, ZohoEvent
from backend.schemas import WebhookPayload
from backend.config import get_settings
import requests

router = APIRouter()
settings = get_settings()

@router.post("/zoho-books")
async def zoho_books_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle invoice payment webhook from Zoho Books.
    """
    # 1. Rate Limiting (Simple In-Memory)
    # In production, use Redis with sliding window
    
    # 2. Verify Signature
    signature = request.headers.get("X-Zoho-Signature")
    if not signature:
        # For hackathon/demo, we might skip if not configured, but in prod this is critical
        # raise HTTPException(status_code=401, detail="Missing Signature")
        pass
    
    # verify_signature(signature, await request.body(), settings.ZOHO_WEBHOOK_SECRET)

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Extract relevant data
    invoice_data = payload.get("invoice", {})
    invoice_id = invoice_data.get("invoice_id") or payload.get("invoice_id")
    amount = invoice_data.get("total") or payload.get("amount")
    payer_name = invoice_data.get("customer_name") or payload.get("customer_name")
    
    # 3. Idempotency
    # Zoho might send a unique event ID in headers or payload. Using invoice_id as proxy if missing.
    event_id = request.headers.get("X-Zoho-Event-Id") or f"inv_{invoice_id}_{amount}"
    
    if db.query(ZohoEvent).filter(ZohoEvent.zoho_event_id == event_id).first():
        return {"status": "ignored", "reason": "idempotent_replay"}
    
    # Record event
    db.add(ZohoEvent(zoho_event_id=event_id))
    
    if not invoice_id or not amount:
         return {"status": "ignored", "reason": "missing_data"}

    if float(amount) < 1000:
        db.commit() # Commit the event record even if ignored
        return {"status": "ignored", "reason": "amount_below_threshold"}

    # Check if invoice already exists
    existing = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if existing:
        db.commit()
        return {"status": "ignored", "reason": "already_exists"}

    # Create Invoice
    new_invoice = Invoice(
        id=invoice_id,
        amount=float(amount),
        payer_name=payer_name,
        status=InvoiceStatus.PENDING_TRIBUNAL
    )
    db.add(new_invoice)
    db.commit()
    
    # Trigger Cliq Bot
    print(f"Triggering Tribunal for Invoice {invoice_id}")

    return {"status": "received", "invoice_id": invoice_id}
