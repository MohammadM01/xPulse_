# xPulse
- Node.js 16+
- PostgreSQL
- Redis
- Zoho Developer Account
- Polygon Amoy Testnet Wallet (with MATIC)
- **[Environment Setup Guide](ENV_SETUP.md)**: Instructions for obtaining API keys.
- **[Deployment Guide](DEPLOYMENT.md)**: How to deploy to Render or use Ngrok.
- **[User Guide](USER_GUIDE.md)**: Step-by-step instructions for the demo flow.
- **[Button Setup Guide](ZOHO_BUTTON_SETUP.md)**: Detailed instructions for configuring the Zoho Books button.
- **[Hackathon Submission Info](SUBMISSION.md)**: Project description and video script.

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

## 🎬 Demo Script (Web2 to Web3 in One Click)

**Step 1: The Trigger**
1.  Open **Zoho Books** and create an Invoice.
2.  Click the **"Mint to Polygon"** button (Custom Button).
3.  *Observation*: You get a success message "✅ Minting Process Started!".

**Step 2: The Blockchain**
1.  The backend immediately hashes the invoice data and submits it to **Polygon**.
2.  *Observation*: The backend logs show the **Transaction Hash**.

**Step 3: Verification**
1.  Open the **xPulse Widget** in Zoho Cliq.
2.  *Observation*: The invoice appears with status **Minted** and a link to **PolygonScan**.

## 🛠️ Troubleshooting
- Ensure Redis is running.
- Check ngrok tunnel status if testing locally.
- Verify wallet has sufficient gas (MATIC).
