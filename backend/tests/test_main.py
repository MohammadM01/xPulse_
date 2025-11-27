import os
import pytest
from unittest.mock import MagicMock, patch

# Set env vars before importing backend.main
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_DB"] = "test_db"
os.environ["ZOHO_BOOKS_AUTHTOKEN"] = "test_token"
os.environ["ZOHO_ORG_ID"] = "test_org"
os.environ["POLYGON_RPC_URL"] = "http://localhost:8545"
os.environ["PRIVATE_KEY"] = "0x0000000000000000000000000000000000000000000000000000000000000000"
os.environ["CONTRACT_ADDRESS"] = "0x0000000000000000000000000000000000000000"

from fastapi.testclient import TestClient
from backend.main import app
from backend.models import Invoice, InvoiceStatus, Vote
from backend.database import get_db

client = TestClient(app)

# Mock DB Session
# We will override this per test

@patch("backend.routers.webhook.get_settings")
def test_zoho_webhook_valid(mock_settings):
    # Mock settings if needed
    mock_settings.return_value.ZOHO_BOOKS_AUTHTOKEN = "test_token"
    
    payload = {
        "invoice": {
            "invoice_id": "INV-TEST-001",
            "total": 5000,
            "customer_name": "Test Corp"
        }
    }
    
    # Create a specific mock for this test
    mock_session = MagicMock()
    # Configure mock: first() returns None (no existing invoice)
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Override dependency to return THIS mock
    app.dependency_overrides[get_db] = lambda: mock_session
    
    response = client.post("/webhooks/zoho-books", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"status": "received", "invoice_id": "INV-TEST-001"}
    
    # Clean up
    app.dependency_overrides = {}

def test_zoho_webhook_low_amount():
    payload = {
        "invoice": {
            "invoice_id": "INV-LOW-001",
            "total": 500, # < 1000
            "customer_name": "Small Corp"
        }
    }
    
    # DB mock not strictly needed if logic checks amount first, but good practice
    mock_session = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_session
    
    response = client.post("/webhooks/zoho-books", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ignored", "reason": "amount_below_threshold"}
    
    app.dependency_overrides = {}

@patch("backend.routers.cliq.Redis")
@patch("backend.routers.cliq.Queue")
def test_cliq_interaction_approve(mock_queue, mock_redis):
    # Mock DB with an existing invoice
    mock_invoice = Invoice(id="INV-001", amount=5000, payer_name="Test", status=InvoiceStatus.PENDING_TRIBUNAL)
    mock_invoice.votes = []
    
    mock_session = MagicMock()
    
    # Define side effect for query()
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Invoice:
            # Found invoice
            mock_query.filter.return_value.first.return_value = mock_invoice
        elif model == Vote:
            # No existing vote
            mock_query.filter.return_value.first.return_value = None
            # Count is 1
            mock_query.filter.return_value.count.return_value = 1
        return mock_query
        
    mock_session.query.side_effect = query_side_effect
    
    app.dependency_overrides[get_db] = lambda: mock_session
    
    payload = {
        "action": "approve",
        "invoice_id": "INV-001",
        "user_id": "USER_A"
    }
    
    response = client.post("/cliq/interaction", json=payload)
    
    assert response.status_code == 200
    assert "1/2 Approvals" in response.json()["text"]
    
    app.dependency_overrides = {}

