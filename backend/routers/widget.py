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
    Return ZML for the sidebar widget showing last 10 invoices.
    """
    invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).limit(10).all()
    
    rows = []
    for inv in invoices:
        status_icon = "✅" if inv.status == "minted" else "⏳" if inv.status == "pending_tribunal" else "❌"
        rows.append({
            "type": "row",
            "children": [
                {"type": "text", "text": f"{status_icon} {inv.id}"},
                {"type": "text", "text": f"${inv.amount}"},
                {"type": "text", "text": inv.status}
            ]
        })

    zml = {
        "type": "page",
        "children": [
            {
                "type": "table",
                "data": rows
            }
        ]
    }
    
    # Wrap in standard ZML response structure if needed by Cliq
    return {"output": zml}
