# 📱 Setting up the xPulse Widget in Zoho Cliq

The **xPulse Widget** lives in your Zoho Cliq sidebar and shows the real-time status of your invoices (Minted vs. Pending).

## Step 1: Open Zoho Cliq Developer Console
1.  Go to [cliq.zoho.com](https://cliq.zoho.com/).
2.  Click your **Profile Picture** (top right) -> **Bots & Tools**.
3.  Click **Widgets** (in the left sidebar).
4.  Click **Create Widget**.

## Step 2: Configure the Widget
*   **Name**: `xPulse Tribunal`
*   **Unique Name**: `xpulse_tribunal` (or similar)
*   **Description**: `View blockchain proof status.`
*   **Access Level**: `Organization` (or `Personal` for testing).
*   Click **Create**.

## Step 3: Connect to Backend
1.  In the widget settings, look for **"Executions"** or **"Handlers"**.
2.  Find the **"On Load"** or **"Widget View"** handler.
3.  Select **"Invoke URL"** (if available) or use **Deluge**.

### Option A: Using Deluge (Recommended)
Paste this code into the Deluge editor for the Widget:

```javascript
// --- REPLACE WITH YOUR RENDER URL ---
backendUrl = "YOUR_RENDER_URL_HERE"; 
// Example: backendUrl = "https://xpulse-api.onrender.com";

response = invokeurl
[
	url : backendUrl + "/api/v1/widget/history"
	type :GET
];

return response.get("output");
```

4.  **Save** the script.

## Step 4: Test It
1.  Go back to the main Zoho Cliq interface.
2.  Look at the **Right Sidebar** (Widgets bar).
3.  Click the **xPulse Tribunal** icon.
4.  You should see the **Minted** and **Pending** tabs!
