# Academic NFT - Startup Guide

## Quick Start

### 1. Start the Backend Server
```bash
# Windows
start-backend.bat

# Unix/Linux/Mac
./start-backend.sh

# Or manually
cd backend
python simple_main.py
```

The backend will start on `http://localhost:8000`

### 2. Start the Frontend Server
```bash
# Windows
start-frontend.bat

# Unix/Linux/Mac
./start-frontend.sh

# Or manually
cd frontend/aptos_frontend
python -m http.server 3000
```

The frontend will be available at `http://localhost:3000`

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Test Page: http://localhost:3000/test-api.html

## Troubleshooting

### Common Issues

#### 1. "Failed to load your NFTs" Error
- **Cause**: Backend server not running or network connectivity issue
- **Solution**: 
  - Ensure backend is running on port 8000
  - Check console for detailed error messages
  - Try refreshing the page

#### 2. "Upload failed: Failed to fetch" Error
- **Cause**: Backend server not running or CORS issue
- **Solution**:
  - Ensure backend is running on port 8000
  - Check if the backend responds: `curl http://localhost:8000/`
  - Clear browser cache and try again

#### 3. Backend Won't Start
- **Cause**: Missing dependencies or port conflict
- **Solution**:
  ```bash
  pip install flask flask-cors
  # Check if port 8000 is available
  netstat -an | grep 8000
  ```

#### 4. Frontend Won't Load
- **Cause**: Port conflict or missing files
- **Solution**:
  - Ensure you're in the correct directory: `frontend/aptos_frontend`
  - Try a different port: `python -m http.server 3001`
  - Check if all files are present

### Testing the Application

1. **Test API Connectivity**:
   - Visit: http://localhost:3000/test-api.html
   - Click the test buttons to verify backend connectivity

2. **Test File Upload**:
   - Go to: http://localhost:3000/student_upload.html
   - Select a file and enter a title
   - Click "Upload File" to test upload functionality

3. **Test NFT Creation**:
   - After uploading, click "Analyze Document"
   - Click "Mint as NFT" to create an NFT
   - Check dashboard for the created NFT

### API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload file
- `POST /analyze` - Analyze uploaded file
- `POST /mint` - Mint NFT
- `GET /nfts` - Get all NFTs
- `POST /feedback` - Submit feedback
- `POST /teacher/comment` - Submit teacher comment

### File Structure

```
plagarism-checker/
├── backend/
│   ├── simple_main.py      # Flask backend server
│   └── uploads/            # Uploaded files
├── frontend/
│   └── aptos_frontend/     # Frontend files
│       ├── js/
│       │   ├── api.js      # API service
│       │   ├── auth.js     # Authentication
│       │   └── app.js      # Main app logic
│       ├── student_upload.html
│       ├── dashboard.html
│       └── test-api.html   # API test page
├── start-backend.bat       # Windows backend starter
├── start-backend.sh        # Unix backend starter
├── start-frontend.bat      # Windows frontend starter
└── start-frontend.sh       # Unix frontend starter
```

### Development Notes

- The backend uses Flask with CORS enabled
- Frontend uses vanilla JavaScript with Tailwind CSS
- All data is stored in memory (not persistent)
- Mock data is loaded from `ipfs_mock/` directory
- File uploads are saved to `backend/uploads/` directory

### Next Steps

1. Implement persistent storage (database)
2. Add real blockchain integration
3. Implement user authentication
4. Add real plagiarism detection algorithms
5. Implement IPFS integration 