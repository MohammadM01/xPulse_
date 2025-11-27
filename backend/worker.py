import redis
from rq import Worker, Queue
from backend.config import get_settings
import time
# from backend.blockchain import mint_proof # To be implemented

settings = get_settings()

listen = ['default']

conn = redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")

def canonical_json_hash(data: dict) -> str:
    import json
    import hashlib
    # Sort keys and remove whitespace
    canonical = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.keccak_256(canonical.encode()).hexdigest() if hasattr(hashlib, 'keccak_256') else hashlib.sha256(canonical.encode()).hexdigest()

def mint_proof_task(invoice_id: str, approver_ids: list):
    """
    Background task to mint proof on Polygon.
    """
    print(f"Starting minting process for Invoice {invoice_id} with approvers {approver_ids}")
    
    from backend.database import SessionLocal
    from backend.models import Invoice, InvoiceStatus
    
    db = SessionLocal()
    try:
        # Canonical Hash
        data_to_hash = {"invoice_id": invoice_id, "approvers": approver_ids}
        data_hash = canonical_json_hash(data_to_hash)
        print(f"Generated Data Hash: {data_hash}")

        # Real Blockchain Interaction
        from backend.blockchain import mint_proof
        tx_hash = mint_proof(invoice_id, approver_ids, data_hash)
        
        print(f"Minted! Tx Hash: {tx_hash}")
        
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            invoice.status = InvoiceStatus.MINTED
            invoice.proof_tx_hash = tx_hash
            db.commit()
            
            # TODO: Update Cliq Message to "Minted"
            print(f"Should update Cliq message for {invoice_id} to SUCCESS")
            
    except Exception as e:
        print(f"❌ Error in minting task: {e}")
        try:
            invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
            if invoice:
                invoice.status = InvoiceStatus.MINT_FAILED
                db.commit()
                # TODO: Update Cliq Message with [Retry] button
                print(f"Should update Cliq message for {invoice_id} to FAILED")
        except Exception as db_e:
            print(f"Critical DB Error: {db_e}")
    finally:
        db.close()

if __name__ == '__main__':
    queues = [Queue(name, connection=conn) for name in listen]
    worker = Worker(queues, connection=conn)
    worker.work()
