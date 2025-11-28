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
    # Debug: Return HTML (easier to render)
    zml = {
        "type": "html",
        "html": "<h1>xPulse Widget Online 🚀</h1><p>If you see this, the connection is working!</p>"
    }
    
    # Return ZML directly
    return zml
