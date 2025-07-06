@echo off
echo Starting Academic NFT Platform...

echo.
echo Starting Backend Server...
start cmd /k "cd backend && python main.py"

echo.
echo Starting Frontend Server...
start cmd /k "cd frontend/aptos_frontend && python -m http.server 3000"

echo.
echo Servers started:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo You can now access the application at http://localhost:3000 