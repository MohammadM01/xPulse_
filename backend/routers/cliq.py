from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.database import get_db
from backend.models import Invoice, Vote, InvoiceStatus
from backend.config import get_settings
from redis import Redis
from rq import Queue
from backend.worker import mint_proof_task

router = APIRouter()
settings = get_settings()

# Redis connection for enqueuing
q = None
if not settings.SYNC_TASKS:
    redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    q = Queue(connection=redis_conn)

@router.post("/interaction")
async def cliq_interaction(request: Request, db: Session = Depends(get_db)):
    """
    Handle actions from Cliq Adaptive Cards.
    """
    # Verify signature (omitted for hackathon)
    
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Cliq sends data in a specific format, often under 'data' or 'action'
    # Simplified handling: assuming payload contains action, invoice_id, user_id
    # In real Cliq, this might be nested in 'arguments' or 'values'
    
    action = payload.get("action")
    invoice_id = payload.get("invoice_id")
    user_id = payload.get("user_id") # Cliq User ID
    
    if not action or not invoice_id or not user_id:
        return {"text": "Error: Missing data"}

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return {"text": "Error: Invoice not found"}

    if action == "approve":
        # 1. Redis Lock to prevent race conditions
        lock = None
        if not settings.SYNC_TASKS:
            lock = redis_conn.lock(f"lock:vote:{invoice_id}", timeout=5)
        
        acquired = False
        try:
            if lock:
                acquired = lock.acquire(blocking=True)
            
            # Check if already voted
            existing_vote = db.query(Vote).filter(Vote.invoice_id == invoice_id, Vote.approver_id == user_id).first()
            if existing_vote:
                 return {"text": "You have already approved this invoice."}
            
            # Record Vote
            new_vote = Vote(invoice_id=invoice_id, approver_id=user_id, vote_type="approve")
            db.add(new_vote)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                return {"text": "You have already approved this invoice."}
            
            # Count votes
            vote_count = db.query(Vote).filter(Vote.invoice_id == invoice_id, Vote.vote_type == "approve").count()
            
            if vote_count == 1:
                return {"type": "update", "text": f"1/2 Approvals (User {user_id}). Waiting for one more."}
            elif vote_count >= 2:
                # Trigger Blockchain Worker
                invoice.status = InvoiceStatus.MINTING
                db.commit()
                
                approvers = [v.approver_id for v in invoice.votes if v.vote_type == "approve"]
                
                if settings.SYNC_TASKS:
                    print("Running task synchronously (No Redis)")
                    mint_proof_task(invoice_id, approvers)
                else:
                    # Retry up to 3 times with backoff (10s, 30s, 60s)
                    from rq import Retry
                    q.enqueue(mint_proof_task, invoice_id, approver_ids, retry=Retry(max=3, interval=[10, 30, 60]))
                
                return {"type": "update", "text": "2/2 Approvals. Minting proof on Polygon..."}
        finally:
            if lock and acquired:
                lock.release()
            
    elif action == "flag":
        invoice.status = InvoiceStatus.REJECTED
        db.commit()
        return {"type": "update", "text": f"Invoice flagged by User {user_id}. Process halted."}

    return {"text": "Unknown action"}

@router.post("/command")
async def cliq_command(request: Request, db: Session = Depends(get_db)):
    """
    Handle Slash Command (e.g., /xpulse)
    """
    # Fetch data
    pending = db.query(Invoice).filter(Invoice.status == "pending_tribunal").order_by(Invoice.created_at.desc()).limit(5).all()
    minted = db.query(Invoice).filter(Invoice.status == "minted").order_by(Invoice.created_at.desc()).limit(5).all()

    text = "### 🔗 Verified On-Chain\n"
    if not minted:
        text += "No minted invoices yet.\n"
    else:
        for inv in minted:
            text += f"* **Invoice #{inv.id}**: ${inv.amount} (✅ Minted)\n"

    text += "\n### ⏳ Pending Approval\n"
    if not pending:
        text += "No pending invoices.\n"
    else:
        for inv in pending:
            text += f"* **Invoice #{inv.id}**: ${inv.amount} (⏳ Pending)\n"

    return {"text": text}
