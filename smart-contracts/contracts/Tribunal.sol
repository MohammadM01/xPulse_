// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Tribunal {
    event ProofMinted(string indexed invoiceId, string[] approverIds, bytes32 dataHash, uint256 timestamp);

    struct Proof {
        string invoiceId;
        string[] approverIds;
        bytes32 dataHash;
        uint256 timestamp;
        bool exists;
    }

    mapping(string => Proof) public proofs;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function mintProof(string memory invoiceId, string[] memory approverIds, bytes32 dataHash) public onlyOwner {
        require(!proofs[invoiceId].exists, "Proof already exists for this invoice");

        proofs[invoiceId] = Proof({
            invoiceId: invoiceId,
            approverIds: approverIds,
            dataHash: dataHash,
            timestamp: block.timestamp,
            exists: true
        });

        emit ProofMinted(invoiceId, approverIds, dataHash, block.timestamp);
    }

    function getProof(string memory invoiceId) public view returns (Proof memory) {
        return proofs[invoiceId];
    }
}
