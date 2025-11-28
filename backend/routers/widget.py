from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Invoice
from backend.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/history")
def widget_history(db: Session = Depends(get_db)):
    """
    Return Rich ZML for the sidebar widget.
    """
    # Fetch data
    pending = db.query(Invoice).filter(Invoice.status == "pending_tribunal").order_by(Invoice.created_at.desc()).limit(5).all()
    minted = db.query(Invoice).filter(Invoice.status == "minted").order_by(Invoice.created_at.desc()).limit(5).all()

    html = """
    <style>
        .card { border: 1px solid #e0e0e0; padding: 12px; margin-bottom: 8px; border-radius: 8px; background: #fff; }
        .minted { color: #00b894; font-weight: bold; }
        .pending { color: #fdcb6e; font-weight: bold; }
        h3 { margin-top: 15px; margin-bottom: 10px; font-family: sans-serif; }
    </style>
    <h3>🔗 Verified On-Chain</h3>
    """

    if not minted:
        html += "<p style='color: #888;'>No minted invoices yet.</p>"
    else:
        for inv in minted:
            html += f"""
            <div class='card'>
                <div style='font-size: 1.1em;'><b>Invoice #{inv.id}</b></div>
                <div>Amount: <b>${inv.amount}</b></div>
                <div class='minted'>✅ Minted</div>
            </div>
            """

    html += "<h3>⏳ Pending Approval</h3>"
    if not pending:
        html += "<p style='color: #888;'>No pending invoices.</p>"
    else:
        for inv in pending:
            html += f"""
            <div class='card'>
                <div style='font-size: 1.1em;'><b>Invoice #{inv.id}</b></div>
                <div>Amount: <b>${inv.amount}</b></div>
                <div class='pending'>⏳ Pending</div>
            </div>
            """

    return {"type": "html", "html": html}
