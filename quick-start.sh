#!/bin/bash

echo "=== Decentralized Academic Plagiarism Checker - Quick Start ==="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed! Please install pip."
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1
APTOS_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS_HERE
NFT_STORAGE_API_KEY=YOUR_NFT_STORAGE_API_KEY_HERE
DEBUG=True
EOF
    echo
    echo "Please edit the .env file with your blockchain credentials."
    echo
fi

# Create necessary directories
mkdir -p uploads corpus ipfs_mock blockchain_mock

echo
echo "Starting the backend server..."
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo
echo "Opening frontend in default browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open frontend/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open frontend/index.html
else
    echo "Could not open browser automatically. Please open frontend/index.html manually."
fi

echo
echo "Application started successfully!"
echo
echo "Backend API: http://localhost:8000"
echo "Frontend: Opened in your browser"
echo
echo "Press Ctrl+C to stop the server when done."

# Wait for Ctrl+C
trap "kill $SERVER_PID; echo 'Server stopped.'; exit 0" INT
wait $SERVER_PID 