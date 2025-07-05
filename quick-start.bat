@echo off
echo === Decentralized Academic Plagiarism Checker - Quick Start ===
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed! Please install pip.
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1 > .env
    echo APTOS_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE >> .env
    echo CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS_HERE >> .env
    echo NFT_STORAGE_API_KEY=YOUR_NFT_STORAGE_API_KEY_HERE >> .env
    echo DEBUG=True >> .env
    echo.
    echo Please edit the .env file with your blockchain credentials.
    echo.
)

REM Create necessary directories
if not exist uploads (
    mkdir uploads
)
if not exist corpus (
    mkdir corpus
)
if not exist ipfs_mock (
    mkdir ipfs_mock
)
if not exist blockchain_mock (
    mkdir blockchain_mock
)

echo.
echo Starting the backend server...
start cmd /k "venv\Scripts\activate.bat && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for server to start
timeout /t 3 > nul

echo.
echo Opening frontend in default browser...
start "" "frontend\index.html"

echo.
echo Application started successfully!
echo.
echo Backend API: http://localhost:8000
echo Frontend: Opened in your browser
echo.
echo Press any key to exit this window...
pause > nul 