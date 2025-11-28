# 🛠️ How to Setup the "Mint to Polygon" Button in Zoho Books

This guide explains exactly how to create the button that connects Zoho Books to your Blockchain backend.

## Step 1: Get your Backend URL (Ngrok)
1.  Look at the terminal window where you ran `ngrok http 8000`.
2.  Find the line that looks like: `Forwarding https://a1b2-c3d4.ngrok-free.app -> http://localhost:8000`.
3.  **Copy** that HTTPS URL (e.g., `https://a1b2-c3d4.ngrok-free.app`).
    *   *Note: This URL changes every time you restart ngrok unless you have a paid account.*

## Step 2: Open Zoho Books Settings
1.  Log in to **Zoho Books**.
2.  Click the **Gear Icon ⚙️** (Settings) in the top-right corner.
3.  You will see a page titled **"All Settings"**.
4.  Scroll down to the **"Module Settings"** section.
5.  Under the **"Sales"** column, click on **"Invoices"**.

## Step 3: Create the Custom Button
1.  Click on the **"Field Customization"** tab.
2.  Click on **"Custom Buttons"**.
3.  Click the **"+ New Custom Button"** button.

## Step 4: Configure the Button
Fill in the details exactly as follows:
*   **Custom Button Name**: `Mint to Polygon`
*   **Position**: Select **"Details View"** (this puts the button inside the invoice page).
*   **Write Deluge Script**: You will see a code editor.

## Step 5: Paste the Script
1.  **Delete** any code that is already in the editor.
2.  **Copy and Paste** the code below:

```javascript
/*
 * Script to Mint Invoice to Polygon
 */

invoiceID = invoice.get("invoice_id");
amount = invoice.get("total");
customerName = invoice.get("customer_name");

// Prepare Payload
payload = Map();
payload.put("invoice_id", invoiceID);
payload.put("amount", amount);
payload.put("payer_name", customerName);

// --- IMPORTANT: REPLACE THE URL BELOW ---
backendUrl = "YOUR_NGROK_URL_HERE"; 
// Example: backendUrl = "https://a1b2-c3d4.ngrok-free.app";

// Call xPulse Backend
response = invokeurl
[
	url : backendUrl + "/api/v1/direct-mint"
	type :POST
	parameters :payload.toString()
    headers : {"Content-Type": "application/json"}
];

info response;

resultMap = Map();

if (response.get("status") == "minting_started") {
	resultMap.put("message", "✅ Minting Process Started!");
    resultMap.put("code", 0); // Success
} else {
	resultMap.put("message", "❌ Error: " + response.get("reason"));
    resultMap.put("code", 1); // Failure
}

return resultMap;
```

## Step 6: Update the URL
1.  In the code you just pasted, find the line:
    ```javascript
    backendUrl = "YOUR_NGROK_URL_HERE";
    ```
2.  Replace `YOUR_NGROK_URL_HERE` with the **Ngrok URL** you copied in Step 1.
    *   **Correct**: `backendUrl = "https://a1b2-c3d4.ngrok-free.app";`
    *   **Incorrect**: `backendUrl = "https://a1b2-c3d4.ngrok-free.app/api/v1/direct-mint";` (Don't add the path here, the script adds it).

## Step 7: Save
1.  Click **Save**.
2.  Go to any **Invoice** in Zoho Books.
3.  You should now see the **"Mint to Polygon"** button at the top!
