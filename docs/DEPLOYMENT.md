# 🚀 Deployment Guide for XPulse Tribunal

For the Zoho CliqTrix Hackathon, you have two main options for deployment:

1.  **Cloud Deployment (Recommended)**: Host your backend on a public cloud provider like **Render** or **Railway**. This ensures your bot is always online.
2.  **Local Tunneling (Fastest for Dev)**: Run everything on your laptop and use **ngrok** to expose it to the internet.

---

## Option 1: Free Cloud Deployment (Render Manual Setup)

This method is **100% FREE** and gives you a permanent URL.

### 1. Prepare your Code
*   Push your code to **GitHub**.

### 2. Create Database (Free PostgreSQL)
1.  Log in to [dashboard.render.com](https://dashboard.render.com/).
2.  Click **New +** -> **PostgreSQL**.
3.  **Name**: `xpulse-db`
4.  **Instance Type**: Select **"Free"**.
5.  Click **Create Database**.
6.  **Wait** for it to be created.
7.  **Copy** the `Internal Database URL` (starts with `postgres://...`).

### 3. Create Web Service (Free)
1.  Click **New +** -> **Web Service**.
2.  Connect your **GitHub repository**.
3.  **Name**: `xpulse-api`
4.  **Instance Type**: Select **"Free"**.
5.  **Build Command**: `pip install -r backend/requirements.txt`
6.  **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
7.  **Environment Variables** (Click "Advanced"):
    *   `PYTHON_VERSION`: `3.9.0`
    *   `SYNC_TASKS`: `true` (This is important! It disables Redis so you don't need to pay).
    *   `DATABASE_URL`: Paste the `Internal Database URL` you copied earlier.
    *   `ZOHO_BOOKS_AUTHTOKEN`: Enter `unused` (We don't need this for the Direct Mint flow).
    *   `ZOHO_ORG_ID`: Enter `unused`.
    *   `POLYGON_RPC_URL`: Your RPC URL.
    *   `PRIVATE_KEY`: Your Wallet Private Key.
    *   `CONTRACT_ADDRESS`: Your deployed contract address.
8.  Click **Create Web Service**.

### 4. Update Zoho
1.  Wait for the deploy to finish (Green "Live" badge).
2.  Copy your new URL (e.g., `https://xpulse-api.onrender.com`).
3.  Update your **Zoho Books Custom Button** with this new URL.

---

## Option 2: Local Tunneling (Ngrok)
Use this if you want to run the demo from your laptop without setting up cloud servers.

### 1. Install Ngrok
*   Download and install [ngrok](https://ngrok.com/).

### 2. Start Backend
*   Run your FastAPI server locally:
    ```bash
    uvicorn backend.main:app --reload
    ```

### 3. Start Tunnel
*   Open a new terminal and run:
    ```bash
    ngrok http 8000
    ```
*   Copy the HTTPS URL (e.g., `https://a1b2-c3d4.ngrok.io`).

### 4. Update Zoho
*   Go to **Zoho Developer Console**.
*   Update the **Bot Endpoint** and **Webhook URL** to use your ngrok URL.
    *   Example: `https://a1b2-c3d4.ngrok.io/api/v1/webhooks/zoho-books`

---

## 🔗 Smart Contract Deployment
Your smart contracts live on the **Polygon Blockchain**, not on a server.

1.  **Deploy**:
    ```bash
    cd smart-contracts
    npx hardhat run scripts/deploy.ts --network amoy
    ```
2.  **Verify**:
    *   Copy the address printed in the terminal.
    *   Update `CONTRACT_ADDRESS` in your backend `.env` (or Render Environment Variables).
