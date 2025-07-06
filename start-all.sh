#!/bin/bash

echo "Starting Academic NFT Platform..."

echo ""
echo "Starting Backend Server..."
cd backend && python main.py &
BACKEND_PID=$!

echo ""
echo "Starting Frontend Server..."
cd ../frontend/aptos_frontend && python -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "Servers started:"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo ""
echo "You can now access the application at http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to press Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 