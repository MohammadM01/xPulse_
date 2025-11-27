const { ethers } = require("ethers");
require("dotenv").config();

// ABI of the Tribunal contract (Simplified for the script)
const ABI = [
    "function mintProof(string memory invoiceId, string[] memory approverIds, bytes32 dataHash) public",
    "event ProofMinted(string indexed invoiceId, string[] approverIds, bytes32 dataHash, uint256 timestamp)"
];

async function main() {
    const args = process.argv.slice(2);
    if (args.length < 3) {
        console.error("Usage: node relayer.js <invoiceId> <approverIds_comma_separated> <dataHash>");
        process.exit(1);
    }

    const invoiceId = args[0];
    const approverIds = args[1].split(",");
    const dataHash = args[2];

    const rpcUrl = process.env.POLYGON_RPC_URL || "https://rpc-amoy.polygon.technology";
    const privateKey = process.env.PRIVATE_KEY;
    const contractAddress = process.env.CONTRACT_ADDRESS;

    if (!privateKey || !contractAddress) {
        console.error("Missing PRIVATE_KEY or CONTRACT_ADDRESS in .env");
        process.exit(1);
    }

    const provider = new ethers.JsonRpcProvider(rpcUrl);
    const wallet = new ethers.Wallet(privateKey, provider);
    const contract = new ethers.Contract(contractAddress, ABI, wallet);

    console.log(`Minting proof for Invoice ${invoiceId}...`);

    try {
        const tx = await contract.mintProof(invoiceId, approverIds, dataHash);
        console.log(`Transaction submitted: ${tx.hash}`);
        await tx.wait();
        console.log("Transaction confirmed!");
        console.log(tx.hash); // Output hash for Python to capture
    } catch (error) {
        console.error("Error minting proof:", error);
        process.exit(1);
    }
}

main();
