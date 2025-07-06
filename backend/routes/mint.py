from fastapi import HTTPException
import os
from typing import Dict, Any
import json
import time
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mock Aptos SDK for compatibility
class MockAptosSDK:
    def __init__(self):
        self.node_url = os.getenv("APTOS_NODE_URL", "https://fullnode.testnet.aptoslabs.com/v1")
        self.private_key = os.getenv("APTOS_PRIVATE_KEY")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")

# Get environment variables
APTOS_NODE_URL = os.getenv("APTOS_NODE_URL", "https://fullnode.testnet.aptoslabs.com/v1")
APTOS_PRIVATE_KEY = os.getenv("APTOS_PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

def mint_nft(metadata: Dict[str, Any]) -> str:
    """
    Mint an NFT on the Aptos blockchain (mock implementation)
    
    Args:
        metadata: NFT metadata including title, summary, plagiarism_score, etc.
        
    Returns:
        Transaction hash
    """
    print("Using mock NFT minting (Aptos SDK not available)")
    
    # For demo purposes, return a mock transaction hash
    mock_tx = f"mock_tx_{uuid.uuid4().hex[:16]}"
    
    # Log the mock transaction
    os.makedirs("blockchain_mock", exist_ok=True)
    with open(f"blockchain_mock/{mock_tx}.json", "w") as f:
        json.dump({
            "type": "mint_nft",
            "metadata": metadata,
            "timestamp": time.time(),
            "status": "mock_success"
        }, f, indent=2)
    
    print(f"Mock transaction created: {mock_tx}")
    return mock_tx