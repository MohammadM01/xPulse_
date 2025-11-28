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
    
    def build_list(invoices, title):
        if not invoices:
            return {"type": "text", "text": f"No {title} invoices found.", "color": "grey"}
            
        elements = []
        for inv in invoices:
            status_icon = "✅" if inv.status == "minted" else "⏳"
            elements.append({
                "type": "text", 
                "text": f"{status_icon} Invoice #{inv.id} | ${inv.amount}",
                "weight": "bold"
            })
            elements.append({
                "type": "text",
                "text": f"Status: {inv.status}",
                "color": "grey"
            })
            elements.append({"type": "divider"})
        
        return {"type": "container", "children": elements}

    # Construct ZML with Tabs
    zml = {
        "type": "tabs",
        "tabs": [
            {
                "title": "Minted 🟢",
                "id": "minted",
                "elements": [
                    {"type": "title", "text": "Verified On-Chain"},
                    build_list(minted, "Minted Invoices")
                ]
            },
            {
                "title": "Pending ⏳",
                "id": "pending",
                "elements": [
                    {"type": "title", "text": "Awaiting Approval"},
                    build_list(pending, "Pending Invoices")
                ]
            }
        ]
    }
    
    return {"output": zml}
