import os
import json
import time
import uuid
import hashlib
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get NFT.Storage API key from environment (will be None since we're not using it)
NFT_STORAGE_API_KEY = os.getenv("NFT_STORAGE_API_KEY")

def upload_to_ipfs(file_path: str, metadata: Dict[str, Any]) -> str:
    """
    Mock IPFS upload function that generates a deterministic CID
    
    Args:
        file_path: Path to the file to upload
        metadata: Metadata to associate with the file
        
    Returns:
        IPFS CID (Content Identifier)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Generate a mock CID based on file content and metadata
    timestamp = int(time.time())
    filename = os.path.basename(file_path)
    
    # Create a unique hash based on file content and metadata
    content_hash = ""
    try:
        with open(file_path, "rb") as f:
            file_content = f.read(1024)  # Read first 1KB for the hash
            content_hash = hashlib.sha256(file_content).hexdigest()[:16]
    except Exception:
        content_hash = hashlib.sha256(filename.encode()).hexdigest()[:16]
    
    # Create a mock CID
    mock_cid = f"bafybeih{content_hash}{timestamp}"
    
    # Store metadata in a local file for reference
    os.makedirs("ipfs_mock", exist_ok=True)
    with open(f"ipfs_mock/{mock_cid}.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Mock IPFS upload successful. CID: {mock_cid}")
    return mock_cid

def get_ipfs_url(cid: str) -> str:
    """
    Get the IPFS URL for a CID
    
    Args:
        cid: IPFS Content Identifier
        
    Returns:
        IPFS URL
    """
    return f"ipfs://{cid}"

def get_ipfs_gateway_url(cid: str, gateway: str = "ipfs.io") -> str:
    """
    Get the HTTP gateway URL for an IPFS CID
    
    Args:
        cid: IPFS Content Identifier
        gateway: IPFS gateway domain
        
    Returns:
        HTTP URL
    """
    return f"https://{gateway}/ipfs/{cid}"