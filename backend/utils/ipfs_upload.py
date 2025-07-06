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

def upload_to_ipfs(file_path: Optional[str], metadata: Dict[str, Any], text_content: Optional[str] = None) -> str:
    """
    Mock IPFS upload function that generates a deterministic CID
    
    Args:
        file_path: Path to the file to upload (optional if text_content is provided)
        metadata: Metadata to associate with the file
        text_content: Text content to upload (optional if file_path is provided)
        
    Returns:
        IPFS CID (Content Identifier)
    """
    # Generate a mock CID based on content and metadata
    timestamp = int(time.time())
    
    # Create a unique hash based on content and metadata
    content_hash = ""
    
    if text_content:
        # Use text content for hash
        content_hash = hashlib.sha256(text_content.encode()).hexdigest()[:16]
    elif file_path and os.path.exists(file_path):
        # Use file content for hash
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "rb") as f:
                file_content = f.read(1024)  # Read first 1KB for the hash
                content_hash = hashlib.sha256(file_content).hexdigest()[:16]
        except Exception:
            content_hash = hashlib.sha256(filename.encode()).hexdigest()[:16]
    else:
        # Use metadata for hash
        content_hash = hashlib.sha256(json.dumps(metadata, sort_keys=True).encode()).hexdigest()[:16]
    
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