from web3 import Web3
from backend.config import get_settings
import json

settings = get_settings()

# Minimal ABI for Tribunal.sol
# function mintProof(string memory invoiceId, string[] memory approverIds, bytes32 dataHash) public
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "invoiceId", "type": "string"},
            {"internalType": "string[]", "name": "approverIds", "type": "string[]"},
            {"internalType": "bytes32", "name": "dataHash", "type": "bytes32"}
        ],
        "name": "mintProof",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def get_web3_provider():
    return Web3(Web3.HTTPProvider(settings.POLYGON_RPC_URL))

def mint_proof(invoice_id: str, approver_ids: list, data_hash: str) -> str:
    """
    Interacts with the Tribunal smart contract to mint a proof.
    Returns the transaction hash.
    """
    w3 = get_web3_provider()
    
    if not w3.is_connected():
        raise Exception("Failed to connect to Polygon RPC")

    account = w3.eth.account.from_key(settings.PRIVATE_KEY)
    contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=CONTRACT_ABI)

    # Prepare Transaction
    # Note: 'data_hash' should be a hex string (0x...)
    if not data_hash.startswith("0x"):
        data_hash = "0x" + data_hash

    nonce = w3.eth.get_transaction_count(account.address)
    
    # Estimate Gas (optional, or use simple defaults for Amoy)
    try:
        gas_estimate = contract.functions.mintProof(invoice_id, approver_ids, data_hash).estimate_gas({
            'from': account.address
        })
    except Exception as e:
        print(f"Gas estimation failed: {e}. Using default gas limit.")
        gas_estimate = 500000 # Fallback

    # Build Transaction
    tx = contract.functions.mintProof(invoice_id, approver_ids, data_hash).build_transaction({
        'chainId': 80002, # Polygon Amoy Testnet Chain ID
        'gas': int(gas_estimate * 1.2), # Buffer
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })

    # Sign Transaction
    signed_tx = w3.eth.account.sign_transaction(tx, settings.PRIVATE_KEY)

    # Send Transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    # Wait for receipt (optional, but good for confirmation)
    # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return w3.to_hex(tx_hash)
