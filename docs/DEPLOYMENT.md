# 🚀 Deployment Guide for XPulse Tribunal

For the Zoho CliqTrix Hackathon, you have two main options for deployment:

1.  **Cloud Deployment (Recommended)**: Host your backend on a public cloud provider like **Render** or **Railway**. This ensures your bot is always online.
2.  **Local Tunneling (Fastest for Dev)**: Run everything on your laptop and use **ngrok** to expose it to the internet.

---

## Option 1: Cloud Deployment (Render.com)
Render is excellent because it supports Python, PostgreSQL, and Redis natively.

### 1. Prepare your Code
*   Ensure you have a `requirements.txt` (we created this).
*   Ensure you have a `Procfile` (optional, but good practice) or just use the start command.
*   Push your code to **GitHub**.

### 2. Create Services on Render
1.  **Sign up** at [render.com](https://render.com).
2.  **New Web Service**:
    *   Connect your GitHub repo.
    *   **Runtime**: Python 3.
    *   **Build Command**: `pip install -r backend/requirements.txt`
    *   **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
    *   **Environment Variables**: Add all variables from your `backend/.env` (POSTGRES_*, REDIS_*, ZOHO_*, POLYGON_*).
3.  **New PostgreSQL**:
    *   Create a managed PostgreSQL database.
    *   Copy the `Internal Database URL` and set it as `DATABASE_URL` in your Web Service environment variables.
4.  **New Redis**:
    *   Create a Redis instance.
    *   Copy the `Internal Redis URL` and set it as `REDIS_URL` in your Web Service.

### 3. Update Zoho
*   Once deployed, Render will give you a URL (e.g., `https://xpulse-tribunal.onrender.com`).
*   Update your **Zoho Books Extension** and **Cliq Bot** to use this new URL instead of `localhost`.

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
