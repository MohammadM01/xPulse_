# XPulse: The Tribunal
- Node.js 16+
- PostgreSQL
- Redis
- Zoho Developer Account
- Polygon Amoy Testnet Wallet (with MATIC)
- **[Environment Setup Guide](ENV_SETUP.md)**: Instructions for obtaining API keys.
- **[Deployment Guide](DEPLOYMENT.md)**: How to deploy to Render or use Ngrok.

### 2. Backend Setup
1.  Navigate to `/backend`.
2.  Create a virtual environment: `python -m venv venv` and activate it.
3.  Install dependencies: `pip install -r requirements.txt`.
4.  Create a `.env` file based on `config.py` variables.
5.  Run the server: `uvicorn backend.main:app --reload`.
6.  Start the Redis worker: `python backend/worker.py`.

### 3. Smart Contract Setup
1.  Navigate to `/smart-contracts`.
2.  Install dependencies: `npm install`.
3.  Create a `.env` file with `POLYGON_RPC_URL` and `PRIVATE_KEY`.
4.  Deploy the contract: `npx hardhat run scripts/deploy.ts --network amoy`.
5.  Copy the deployed contract address to your backend `.env`.

### 4. Zoho Configuration
1.  **Zoho Books**: Create an extension using `/zoho-assets/manifest.json`.
2.  **Zoho Cliq**: Create a Bot named "Tribunal".
    - Use `/zoho-assets/bot_handler.deluge` for the bot logic.
    - Configure the Message Handler and Button Actions to point to your backend URL (use ngrok for local dev).

## 🎬 Demo Script (For Judges)

**Step 1: The Trigger**
1.  Open **Zoho Books**.
2.  Create a new Invoice for **$5,000** (must be > $1,000).
3.  Mark the invoice as **Paid**.
4.  *Observation*: The **XPulse Bot** in Zoho Cliq posts an "🚨 Tribunal Activated" card.

**Step 2: The Tribunal (Multi-Sig)**
1.  **User A** (You) clicks `[✅ Approve]` on the card.
    - *Observation*: Card updates to "1/2 Approvals (User A)".
2.  **User B** (Another account or simulated) clicks `[✅ Approve]`.
    - *Observation*: Card updates to "2/2 Approvals. Minting...".

**Step 3: The Blockchain**
1.  Wait for a few seconds.
2.  The backend worker signs the transaction and submits it to Polygon Amoy.
3.  *Observation*: The Cliq card updates with a **Green Badge** and a link to **PolygonScan**.

**Step 4: The Widget**
1.  Open the **XPulse Widget** in the Cliq sidebar.
2.  *Observation*: See the list of verified invoices with their on-chain status.

## 🛠️ Troubleshooting
- Ensure Redis is running.
- Check ngrok tunnel status if testing locally.
- Verify wallet has sufficient gas (MATIC).
