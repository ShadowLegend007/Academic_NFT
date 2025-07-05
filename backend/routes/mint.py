from fastapi import HTTPException
import os
from typing import Dict, Any
import json
import time
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Aptos SDK
try:
    from aptos_sdk.account import Account
    from aptos_sdk.client import RestClient
    from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload
    from aptos_sdk.type_tag import TypeTag, StructTag
except ImportError:
    raise ImportError("Aptos SDK not installed. Run 'pip install aptos-sdk'")

# Get environment variables
APTOS_NODE_URL = os.getenv("APTOS_NODE_URL", "https://fullnode.testnet.aptoslabs.com/v1")
APTOS_PRIVATE_KEY = os.getenv("APTOS_PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

def mint_nft(metadata: Dict[str, Any]) -> str:
    """
    Mint an NFT on the Aptos blockchain
    
    Args:
        metadata: NFT metadata including title, summary, plagiarism_score, etc.
        
    Returns:
        Transaction hash
    """
    if not APTOS_PRIVATE_KEY:
        print("Warning: APTOS_PRIVATE_KEY not set. Using mock transaction.")
        # For demo purposes, return a mock transaction hash
        mock_tx = f"mock_tx_{uuid.uuid4().hex[:16]}"
        
        # Log the mock transaction
        os.makedirs("blockchain_mock", exist_ok=True)
        with open(f"blockchain_mock/{mock_tx}.json", "w") as f:
            json.dump({
                "type": "mint_nft",
                "metadata": metadata,
                "timestamp": time.time()
            }, f, indent=2)
        
        print(f"Mock transaction created: {mock_tx}")
        return mock_tx
    
    try:
        # Initialize Aptos client
        rest_client = RestClient(APTOS_NODE_URL)
        
        # Create account from private key
        account = Account.load_key(APTOS_PRIVATE_KEY)
        
        if not CONTRACT_ADDRESS:
            print("Warning: CONTRACT_ADDRESS not set. Using account address.")
            contract_address = account.address()
        else:
            contract_address = CONTRACT_ADDRESS
        
        # Prepare arguments for the mint function
        args = [
            TransactionArgument(metadata["title"], TransactionArgument.STRING),
            TransactionArgument(metadata["summary"], TransactionArgument.STRING),
            TransactionArgument(int(metadata["plagiarism_score"] * 100), TransactionArgument.U64),
            TransactionArgument(metadata["ipfs_cid"], TransactionArgument.STRING),
            TransactionArgument(int(metadata["timestamp"]), TransactionArgument.U64),
            TransactionArgument(metadata["wallet_address"], TransactionArgument.ADDRESS)
        ]
        
        # Create transaction payload
        payload = TransactionPayload(
            EntryFunction.natural(
                f"{contract_address}::AcademicNFT",
                "mint",
                [],
                args
            )
        )
        
        # Submit transaction
        signed_transaction = rest_client.create_bcs_signed_transaction(
            account, payload
        )
        tx_hash = rest_client.submit_bcs_transaction(signed_transaction)
        
        # Wait for transaction to complete
        rest_client.wait_for_transaction(tx_hash)
        
        print(f"NFT minted successfully. Transaction hash: {tx_hash}")
        return tx_hash
    except Exception as e:
        print(f"Error minting NFT: {str(e)}")
        # For demo purposes, return a mock transaction hash on error
        mock_tx = f"mock_tx_{uuid.uuid4().hex[:16]}"
        
        # Log the error
        os.makedirs("blockchain_mock", exist_ok=True)
        with open(f"blockchain_mock/{mock_tx}_error.json", "w") as f:
            json.dump({
                "type": "mint_nft_error",
                "metadata": metadata,
                "error": str(e),
                "timestamp": time.time()
            }, f, indent=2)
        
        print(f"Mock transaction created due to error: {mock_tx}")
        return mock_tx