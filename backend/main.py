from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import os
import shutil
from typing import Optional, Dict, Any
import json
from datetime import datetime
from pydantic import BaseModel

# Import route handlers
from routes.upload import handle_upload, extract_text_from_file
from routes.analyze import analyze_document
from routes.mint import mint_nft

# Import utilities
from utils.plagiarism_check import check_plagiarism
from utils.summarizer import generate_summary
from utils.ipfs_upload import upload_to_ipfs

# Create request models
class AnalyzeRequest(BaseModel):
    file_id: str

class MintRequest(BaseModel):
    title: str
    summary: str
    plagiarism_score: float
    wallet_address: str
    ipfs_cid: str
    timestamp: str

class FeedbackRequest(BaseModel):
    nft_id: str
    feedback: str
    teacher_address: str

# Create FastAPI app
app = FastAPI(title="Decentralized Academic Plagiarism Checker")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("corpus", exist_ok=True)

# In-memory storage for demo purposes
# In a production app, use a database
uploaded_files = {}
nfts = []

@app.get("/")
async def read_root():
    return {"message": "Decentralized Academic Plagiarism Checker API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), title: str = Form(...)):
    # Generate a unique ID for the file
    file_id = str(uuid.uuid4())
    
    # Save the file
    file_path = f"uploads/{file_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text from the file
    try:
        text = extract_text_from_file(file_path)
        
        # Store file info in memory
        uploaded_files[file_id] = {
            "id": file_id,
            "filename": file.filename,
            "title": title,
            "path": file_path,
            "text": text,
            "upload_time": datetime.now().isoformat()
        }
        
        return {"file_id": file_id, "message": "File uploaded successfully"}
    except Exception as e:
        # Clean up the file if text extraction fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.post("/analyze")
async def analyze_file(request: AnalyzeRequest):
    file_id = request.file_id
    if not file_id or file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_info = uploaded_files[file_id]
    text = file_info["text"]
    
    try:
        print(f"Starting analysis for file: {file_info['filename']}")
        
        # Check plagiarism
        print("Running plagiarism check...")
        plagiarism_score = check_plagiarism(text)
        print(f"Plagiarism score: {plagiarism_score}")
        
        # Generate summary
        print("Generating summary...")
        summary = generate_summary(text)
        print(f"Summary generated: {summary[:50]}...")
        
        # Upload to IPFS
        print("Uploading to IPFS...")
        metadata = {
            "title": file_info["title"],
            "text": text,
            "summary": summary,
            "plagiarism_score": plagiarism_score,
            "timestamp": datetime.now().isoformat()
        }
        
        ipfs_cid = upload_to_ipfs(file_info["path"], metadata)
        print(f"IPFS upload complete. CID: {ipfs_cid}")
        
        # Return results
        return {
            "plagiarism_score": plagiarism_score,
            "summary": summary,
            "ipfs_cid": ipfs_cid
        }
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/mint")
async def mint_academic_nft(request: MintRequest):
    # Convert Pydantic model to dict for the mint_nft function
    request_dict = request.dict()
    
    # Mint NFT on Aptos blockchain
    try:
        transaction_hash = mint_nft(request_dict)
        
        # Store NFT info
        nft_id = str(uuid.uuid4())
        nft = {
            "id": nft_id,
            "title": request.title,
            "summary": request.summary,
            "plagiarism_score": request.plagiarism_score,
            "wallet_address": request.wallet_address,
            "ipfs_cid": request.ipfs_cid,
            "timestamp": request.timestamp,
            "transaction_hash": transaction_hash,
            "feedback": None
        }
        nfts.append(nft)
        
        return {
            "success": True,
            "nft_id": nft_id,
            "transaction_hash": transaction_hash
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error minting NFT: {str(e)}")

@app.get("/nfts")
async def get_nfts():
    return nfts

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    nft_id = request.nft_id
    feedback = request.feedback
    teacher_address = request.teacher_address
    
    # Find the NFT
    for nft in nfts:
        if nft["id"] == nft_id:
            # Update feedback
            nft["feedback"] = feedback
            nft["teacher_address"] = teacher_address
            nft["feedback_time"] = datetime.now().isoformat()
            
            return {"success": True, "message": "Feedback submitted successfully"}
    
    raise HTTPException(status_code=404, detail="NFT not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)