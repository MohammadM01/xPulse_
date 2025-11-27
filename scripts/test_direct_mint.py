import requests
import time
import subprocess
import sys
import os

# Ensure we are in the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000/api/v1"

def start_server():
    print("🚀 Starting Backend Server...")
    # Start uvicorn in a subprocess
    f = open("server.log", "w")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "localhost", "--port", "8000"],
        stdout=f,
        stderr=subprocess.STDOUT
    )
    time.sleep(5) # Wait for startup
    return process

def test_direct_mint():
    print("\n--- 🧪 Testing Direct Mint Feature ---")
    
    invoice_id = "INV-MANUAL-001"
    payload = {
        "invoice_id": invoice_id,
        "amount": 5000.0,
        "payer_name": "Manual Trigger Corp"
    }

    try:
        print(f"1️⃣  Triggering Direct Mint for {invoice_id}...")
        res = requests.post(f"{BASE_URL}/direct-mint", json=payload)
        print(f"   Response: {res.status_code} - {res.json()}")
        
        if res.status_code == 200 and res.json().get("status") == "minting_started":
            print("   ✅ API Request Successful")
        else:
            print("   ❌ API Request Failed")
            return

        print("2️⃣  Checking Widget History (to verify minting)...")
        # Wait for worker to process (sync mode)
        time.sleep(2) 
        
        res = requests.get(f"{BASE_URL}/widget/history?user_id=test_user")
        if invoice_id in res.text:
             print("   ✅ Found Invoice in Widget! (Minted)")
        else:
             print(f"   ❌ Invoice not found in widget. Response: {res.text[:100]}...")

    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    # Check if server is running
    proc = None
    try:
        requests.get(BASE_URL.replace("/api/v1", ""), timeout=2)
        print("Server already running.")
    except:
        proc = start_server()

    try:
        test_direct_mint()
    finally:
        if proc:
            print("🛑 Stopping Server...")
            proc.terminate()
