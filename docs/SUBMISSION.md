# 🏆 Hackathon Submission Guide

## 1. Project Category
**Category**: **Zoho Cliq Extension** (Integrations)
**Name**: xPulse

## 2. Short Description (Pitch)
XPulse is a **Forensic Auditor Bot** that bridges **Zoho Books** and **Polygon Blockchain**. It automatically secures high-value invoices by minting a cryptographic proof of payment on-chain, ensuring immutable audit trails and preventing fraud.

## 3. Long Description
In the age of AI and digital finance, trust is paramount. xPulse brings **Web3 security** to the **Web2 world** of Zoho.

**Key Features:**
*   **Seamless Bridge**: A "Mint to Polygon" button directly inside Zoho Books.
*   **Multi-Sig Security**: A "Tribunal" bot in Zoho Cliq that requires multiple approvals for high-value transactions.
*   **Immutable Proof**: Every verified invoice is hashed and stored on the Polygon Blockchain (Amoy Testnet).
*   **Real-Time Widget**: A Zoho Cliq widget to view the on-chain status of all invoices instantly.

**Tech Stack:**
*   **Backend**: Python (FastAPI), PostgreSQL, Redis.
*   **Blockchain**: Solidity (Smart Contracts), Polygon Amoy, Web3.py.
*   **Zoho**: Deluge (Custom Actions), ZML (Widgets), Adaptive Cards.

## 4. Video Demo Script (1-2 Minutes)

**[Scene 1: The Problem]**
*   *Voiceover*: "Invoices can be tampered with. Audits are slow. How do we prove a payment happened without a doubt?"

**[Scene 2: The Trigger (Zoho Books)]**
*   *Action*: Show creating an invoice in Zoho Books.
*   *Action*: Click the **"Mint to Polygon"** button.
*   *Voiceover*: "With xPulse, you can secure an invoice on the blockchain with just one click directly from Zoho Books."

**[Scene 3: The Magic (Backend/Logs)]**
*   *Action*: Show the terminal logs scrolling (Minting... Success!).
*   *Action*: Show the **PolygonScan** transaction page.
*   *Voiceover*: "xPulse hashes the data and mints a permanent proof on Polygon. It's immutable and verifiable."

**[Scene 4: The Verification (Zoho Cliq)]**
*   *Action*: Open the **xPulse Widget** in Cliq. Show the "Minted" tab.
*   *Voiceover*: "And your team can verify the status instantly inside Zoho Cliq using our custom widget. Web2 simplicity, Web3 security."

**[Scene 5: Closing]**
*   *Voiceover*: "xPulse. Trust, verified."
