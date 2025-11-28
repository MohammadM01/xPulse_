from fastapi import FastAPI
from backend.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Create tables on startup (for SQLite demo)
from backend.database import engine, Base
import backend.models # Import models to register them with Base
Base.metadata.create_all(bind=engine)

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Welcome to xPulse API"}

from backend.routers import webhook, cliq, widget, direct_mint
app.include_router(webhook.router, prefix=settings.API_V1_STR + "/webhooks", tags=["webhooks"])
app.include_router(cliq.router, prefix=settings.API_V1_STR + "/cliq", tags=["cliq"])
app.include_router(widget.router, prefix=settings.API_V1_STR + "/widget", tags=["widget"])
app.include_router(direct_mint.router, prefix=settings.API_V1_STR, tags=["direct-mint"])
