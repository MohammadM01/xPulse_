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
    # Debug: Return simple text to verify rendering
    zml = {
        "type": "text",
        "text": "xPulse Widget is Online! 🚀"
    }
    
    return {"output": zml}
