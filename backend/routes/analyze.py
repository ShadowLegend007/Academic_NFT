from fastapi import HTTPException
from typing import Dict, Any

from utils.plagiarism_check import check_plagiarism
from utils.summarizer import generate_summary
from utils.ipfs_upload import upload_to_ipfs

async def analyze_document(text: str, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a document for plagiarism, generate a summary, and upload to IPFS
    
    Args:
        text: The extracted text from the document
        file_path: Path to the uploaded file
        metadata: Additional metadata about the document
        
    Returns:
        Dict containing plagiarism score, summary, and IPFS CID
    """
    try:
        # Check for plagiarism
        plagiarism_score = check_plagiarism(text)
        
        # Generate summary
        summary = generate_summary(text)
        
        # Add analysis results to metadata
        metadata["text"] = text
        metadata["summary"] = summary
        metadata["plagiarism_score"] = plagiarism_score
        
        # Upload to IPFS
        ipfs_cid = upload_to_ipfs(file_path, metadata)
        
        return {
            "plagiarism_score": plagiarism_score,
            "summary": summary,
            "ipfs_cid": ipfs_cid
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing document: {str(e)}"
        )