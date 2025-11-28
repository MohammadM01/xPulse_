# 📘 xPulse User Guide: From Zoho to Blockchain

This guide walks you through the complete flow of creating an invoice in Zoho Books and minting it on the Polygon Blockchain.

## Prerequisites
1.  **Backend Running**: Ensure your backend is running and exposed via **ngrok**.
2.  **Zoho Configured**: Ensure your "Mint to Polygon" button script is updated with your ngrok URL.

---

## Step 1: Create an Invoice in Zoho Books
1.  Log in to your **Zoho Books** account.
2.  Navigate to **Sales** -> **Invoices**.
3.  Click **+ New**.
4.  **Customer Name**: Select or create a customer (e.g., "Demo Client").
5.  **Items**: Add a line item.
    *   **Note**: Ensure the total amount is **> $1,000** if you want to test the "Tribunal" (Webhook) flow, as the code ignores small amounts.
6.  Click **Save as Draft** or **Save and Send**.

## Step 2: Trigger the Blockchain Flow (One Click)

1.  Open the Invoice you just created in Zoho Books.
2.  Click the **"Mint to Polygon"** custom button (top right).
3.  You should see a success message: "✅ Minting Process Started!".
4.  The system automatically:
    *   Hashes the invoice data.
    *   Signs the transaction.
    *   Mints the proof to the Polygon Blockchain.

---

## Step 3: Verify on Blockchain
1.  Check your **Backend Terminal Logs**. Look for:
    ```
    Minted! Tx Hash: 0x123abc...
    ```
2.  Copy the **Tx Hash**.
3.  Go to [PolygonScan Amoy](https://amoy.polygonscan.com/).
4.  Paste the hash in the search bar.
5.  Verify that the status is **Success** and the `ProofMinted` event is present.

---

## Step 4: Verify in Widget
1.  Open **Zoho Cliq**.
2.  Open the **xPulse Widget** in the sidebar.
3.  You should see your invoice listed with a "Minted" status and a link to the transaction.
