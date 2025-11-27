import requests
import time
import subprocess
import sys
import os
import signal

# Configuration
BASE_URL = "http://localhost:8000"
INVOICE_ID = "INV-DEMO-001"

def start_server():
    print("🚀 Starting Backend Server...")
    # Set env var to enable synchronous tasks
    env = os.environ.copy()
    env["SYNC_TASKS"] = "True"
    # Use dummy values for required env vars if not set
    # if "POSTGRES_USER" not in env:
    #     # env["DATABASE_URL"] = "sqlite:///./sql_app.db" # Commented out to use real Postgres
    #     env["POSTGRES_USER"] = "postgres" 
    #     env["POSTGRES_PASSWORD"] = "password"
    #     env["POSTGRES_SERVER"] = "localhost"
    #     env["POSTGRES_DB"] = "xpulse_tribunal"
    #     env["ZOHO_BOOKS_AUTHTOKEN"] = "dummy"
    #     env["ZOHO_ORG_ID"] = "dummy"
    #     env["POLYGON_RPC_URL"] = "http://dummy"
    #     env["PRIVATE_KEY"] = "dummy"
    #     env["CONTRACT_ADDRESS"] = "dummy"

    f = open("server.log", "w")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"],
        env=env,
        stdout=f,
        stderr=subprocess.STDOUT
    )
    time.sleep(5) # Wait for startup
    return process

def stop_server(process):
    print("🛑 Stopping Server...")
    process.terminate()

def run_simulation():
    print(f"\n--- 🎬 Starting XPulse Simulation ---\n")

    # 1. Trigger Webhook
    print(f"1️⃣  Simulating Zoho Books Webhook for {INVOICE_ID}...")
    webhook_payload = {
        "invoice": {
            "invoice_id": INVOICE_ID,
            "total": 5000,
            "customer_name": "Demo Corp"
        }
    }
    try:
        res = requests.post(f"{BASE_URL}/webhooks/zoho-books", json=webhook_payload)
        print(f"   Response: {res.status_code} - {res.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        if 'res' in locals():
            print(f"   Response Text: {res.text}")
        return

    time.sleep(1)

    # 2. User A Approval
    print(f"\n2️⃣  User A (Alice) Approves...")
    cliq_payload_a = {
        "action": "approve",
        "invoice_id": INVOICE_ID,
        "user_id": "USER_ALICE"
    }
    res = requests.post(f"{BASE_URL}/cliq/interaction", json=cliq_payload_a)
    print(f"   Response: {res.json().get('text')}")

    time.sleep(1)

    # 3. User B Approval
    print(f"\n3️⃣  User B (Bob) Approves (Triggering Minting)...")
    cliq_payload_b = {
        "action": "approve",
        "invoice_id": INVOICE_ID,
        "user_id": "USER_BOB"
    }
    res = requests.post(f"{BASE_URL}/cliq/interaction", json=cliq_payload_b)
    print(f"   Response: {res.json().get('text')}")

    time.sleep(3) # Wait for "minting" (mocked sleep in worker)

    # 4. Check Widget History
    print(f"\n4️⃣  Checking Widget History...")
    res = requests.get(f"{BASE_URL}/widget/history")
    data = res.json()
    
    # Simple check if invoice is in the list
    found = False
    if "output" in data and "children" in data["output"]:
        rows = data["output"]["children"][0]["data"]
        for row in rows:
            cols = row["children"]
            # cols[0] is ID, cols[2] is Status
            if INVOICE_ID in cols[0]["text"]:
                print(f"   ✅ Found Invoice in Widget!")
                print(f"   Status: {cols[2]['text']}")
                found = True
                break
    
    if not found:
        print("   ⚠️ Invoice not found in widget history.")

    print(f"\n--- ✅ Simulation Complete ---")

if __name__ == "__main__":
    # Check if server is already running
    try:
        requests.get(BASE_URL, timeout=2)
        print("Server already running. Using existing instance.")
        run_simulation()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        proc = start_server()
        try:
            run_simulation()
        finally:
            stop_server(proc)
