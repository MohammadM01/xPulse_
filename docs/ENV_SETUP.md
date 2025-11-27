# 🔑 Environment Setup Guide

This guide explains how to obtain the necessary keys and secrets for your `.env` files.

## 1. Zoho Books Configuration

### A. Organization ID (`ZOHO_ORG_ID`)
1.  Log in to [Zoho Books](https://books.zoho.com/).
2.  Click on your profile picture in the top right.
3.  Copy the **Organization ID** (usually a numeric string).

### B. Auth Token (`ZOHO_BOOKS_AUTHTOKEN`)
*Note: Zoho has moved to OAuth 2.0. For this hackathon project, we will generate a temporary **Access Token** using the Self-Client option.*

1.  Go to the [Zoho API Console](https://api-console.zoho.com/).
2.  Click **Add Client** -> **Self Client**.
3.  In the **Scope** field, enter: `ZohoBooks.invoices.CREATE,ZohoBooks.invoices.READ,ZohoBooks.invoices.UPDATE` (adjust based on needs).
4.  Set **Scope Description** to "XPulse Hackathon".
5.  Click **Create**.
6.  Copy the **Generate Code**.
7.  Use the generated code to get an access token (valid for 1 hour) or follow the [Zoho OAuth Guide](https://www.zoho.com/books/api/v3/#oauth) for a permanent refresh token setup.
    *   *Quick Hack*: For testing, you can generate an Access Token directly if the UI allows, or use the "Generate Code" tab to get a code and exchange it via Postman.

## 2. Blockchain Configuration (Polygon Amoy)

### A. RPC URL (`POLYGON_RPC_URL`)
You need a connection to the Polygon Amoy Testnet.
*   **Option 1 (Public)**: Use a public RPC URL from [Chainlist](https://chainlist.org/chain/80002).
    *   Example: `https://rpc-amoy.polygon.technology`
*   **Option 2 (Recommended)**: Sign up for [Alchemy](https://www.alchemy.com/) or [Infura](https://www.infura.io/).
    1.  Create a new App (Chain: Polygon POS, Network: Amoy).
    2.  Copy the **HTTPS** key.

### B. Private Key (`PRIVATE_KEY`)
**⚠️ WARNING: Use a dedicated TEST WALLET. Never use a wallet holding real funds.**

1.  Open **MetaMask** (or your preferred wallet).
2.  Select the account you want to use.
3.  Click the three dots menu -> **Account details**.
4.  Click **Show private key**.
5.  Enter your password and copy the key.
6.  **Paste this into your `.env` file.**

### C. Contract Address (`CONTRACT_ADDRESS`)
This is generated *after* you deploy your smart contract.

1.  Ensure `POLYGON_RPC_URL` and `PRIVATE_KEY` are set in `smart-contracts/.env`.
2.  Run the deployment script:
    ```bash
    cd smart-contracts
    npx hardhat run scripts/deploy.ts --network amoy
    ```
3.  The output will show: `Tribunal deployed to 0x...`
4.  Copy this address to your `backend/.env`.

## 3. Database (`POSTGRES_...`)
If running locally with the provided `docker-compose` (if applicable) or local Postgres:
*   **User/Password**: Whatever you configured during Postgres installation (default often `postgres`/`password`).
*   **DB Name**: Create a database named `xpulse_tribunal` using pgAdmin or command line: `CREATE DATABASE xpulse_tribunal;`
