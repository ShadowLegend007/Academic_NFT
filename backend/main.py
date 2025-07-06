from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import json
from datetime import datetime
import shutil

app = Flask(__name__)
CORS(app)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("corpus", exist_ok=True)

# In-memory storage for demo purposes
uploaded_files = {}
nfts = []

def load_mock_ipfs_documents():
    """Load previously checked documents from ipfs_mock folder"""
    mock_documents = []
    ipfs_mock_dir = "../ipfs_mock"
    
    try:
        if os.path.exists(ipfs_mock_dir):
            for filename in os.listdir(ipfs_mock_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(ipfs_mock_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        # Create a mock NFT entry from the IPFS data
                        mock_nft = {
                            "id": filename.replace('.json', ''),
                            "title": data.get('title', 'Untitled Document'),
                            "summary": data.get('summary', ''),
                            "plagiarism_score": data.get('plagiarism_score', 0.0),
                            "wallet_address": "mock_wallet_address",
                            "ipfs_cid": filename.replace('.json', ''),
                            "timestamp": data.get('timestamp', ''),
                            "transaction_hash": f"mock_tx_{filename.replace('.json', '')}",
                            "feedback": None,
                            "filename": f"{data.get('title', 'document')}.txt",
                            "student_name": "Previous User",
                            "user_email": "previous@example.com",
                            "teacher_feedback": None,
                            "is_mock": True
                        }
                        mock_documents.append(mock_nft)
                    except Exception as e:
                        print(f"Error loading mock document {filename}: {e}")
    except Exception as e:
        print(f"Error accessing ipfs_mock directory: {e}")
    
    return mock_documents

# Load mock documents on startup
mock_documents = load_mock_ipfs_documents()
nfts.extend(mock_documents)

@app.route('/')
def read_root():
    return jsonify({"message": "Decentralized Academic Plagiarism Checker API"})

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        title = request.form.get('title', 'Untitled')
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())
        
        # Save the file
        file_path = f"uploads/{file_id}_{file.filename}"
        file.save(file_path)
        
        # Extract text from the file (simplified)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except:
            text = "Text extraction not available for this file type"
        
        # Store file info in memory
        uploaded_files[file_id] = {
            "id": file_id,
            "filename": file.filename,
            "title": title,
            "path": file_path,
            "text": text,
            "upload_time": datetime.now().isoformat()
        }
        
        return jsonify({"file_id": file_id, "message": "File uploaded successfully"})
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze_file():
    try:
        print(f"Received analyze request: {request.data}")
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        file_id = data.get('file_id')
        print(f"File ID: {file_id}")
        
        if not file_id or file_id not in uploaded_files:
            print(f"File not found: {file_id}")
            print(f"Available files: {list(uploaded_files.keys())}")
            return jsonify({"error": "File not found"}), 404
        
        file_info = uploaded_files[file_id]
        text = file_info["text"]
        
        print(f"Starting analysis for file: {file_info['filename']}")
        
        # Mock plagiarism check (simplified)
        import random
        plagiarism_score = random.uniform(0.0, 0.3)  # Mock low plagiarism score
        
        # Mock summary
        summary = f"This is a mock summary for {file_info['title']}. The document appears to be original work with minimal similarity to existing sources."
        
        # Mock IPFS CID
        ipfs_cid = f"mock_cid_{file_id}"
        
        print(f"Analysis complete. Plagiarism score: {plagiarism_score}")
        
        result = {
            "plagiarism_score": plagiarism_score,
            "summary": summary,
            "ipfs_cid": ipfs_cid
        }
        print(f"Returning result: {result}")
        
        return jsonify(result)
    except Exception as e:
        import traceback
        print(f"Analysis failed: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/mint', methods=['POST'])
def mint_nft():
    try:
        print(f"Received mint request: {request.data}")
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            # Convert string to float if needed
            if 'plagiarism_score' in data and isinstance(data['plagiarism_score'], str):
                try:
                    data['plagiarism_score'] = float(data['plagiarism_score'])
                except ValueError:
                    data['plagiarism_score'] = 0.0
        
        print(f"Mint data: {data}")
        
        # Create NFT entry
        nft_id = str(uuid.uuid4())
        nft = {
            "id": nft_id,
            "title": data.get('title', 'Untitled'),
            "summary": data.get('summary', ''),
            "plagiarism_score": data.get('plagiarism_score', 0.0),
            "wallet_address": data.get('wallet_address', 'mock_wallet'),
            "ipfs_cid": data.get('ipfs_cid', ''),
            "timestamp": data.get('timestamp', datetime.now().isoformat()),
            "transaction_hash": f"mock_tx_{nft_id}",
            "feedback": None,
            "student_name": "Current User",
            "user_email": "user@example.com",
            "teacher_feedback": None
        }
        
        nfts.append(nft)
        
        result = {
            "nft_id": nft_id,
            "transaction_hash": nft["transaction_hash"],
            "message": "NFT minted successfully"
        }
        print(f"Mint successful: {result}")
        
        return jsonify(result)
    except Exception as e:
        import traceback
        print(f"Minting failed: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": f"Minting failed: {str(e)}"}), 500

@app.route('/nfts', methods=['GET'])
def get_nfts():
    try:
        return jsonify(nfts)
    except Exception as e:
        return jsonify({"error": f"Failed to get NFTs: {str(e)}"}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        nft_id = data.get('nft_id')
        feedback = data.get('feedback')
        
        # Find and update NFT
        for nft in nfts:
            if nft['id'] == nft_id:
                nft['feedback'] = feedback
                return jsonify({"message": "Feedback submitted successfully"})
        
        return jsonify({"error": "NFT not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to submit feedback: {str(e)}"}), 500

@app.route('/teacher/comment', methods=['POST'])
def submit_teacher_comment():
    try:
        data = request.get_json()
        nft_id = data.get('nft_id')
        feedback = data.get('feedback')
        
        # Find and update NFT
        for nft in nfts:
            if nft['id'] == nft_id:
                nft['teacher_feedback'] = feedback
                return jsonify({"message": "Teacher comment submitted successfully"})
        
        return jsonify({"error": "NFT not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to submit teacher comment: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask backend server...")
    print("📚 API will be available at http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True) 