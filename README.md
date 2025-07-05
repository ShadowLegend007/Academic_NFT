# Decentralized Academic Plagiarism Checker

A decentralized web application that allows students to check their academic papers for plagiarism, get AI-generated summaries, and mint their work as NFTs on the Aptos blockchain.

## 🔧 Tech Stack

### Frontend
- HTML + Bootstrap + Vanilla JavaScript
- Aptos Wallet Adapter for wallet connection

### Backend
- Python FastAPI
- TF-IDF and cosine similarity for plagiarism detection
- HuggingFace T5/Pegasus for text summarization

### Storage
- IPFS via mock implementation (can be upgraded to nft.storage)

### Blockchain
- Aptos Move smart contract for NFT minting
- Petra/Martian Wallet integration

## 📂 Project Structure

```
/frontend
├── index.html
├── teacher.html
├── styles.css
├── app.js

/backend
├── main.py
├── routes/
│   ├── upload.py
│   ├── analyze.py
│   └── mint.py
├── utils/
│   ├── plagiarism_check.py
│   ├── summarizer.py
│   └── ipfs_upload.py
├── corpus/
└── models/

/contracts
└── AcademicNFT.move

.env.example
README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Node.js (for blockchain setup script)
- Aptos CLI (for contract deployment)
- Petra or Martian wallet browser extension

### Backend Setup
1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following content:
   ```
   APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1
   APTOS_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
   CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS_HERE
   NFT_STORAGE_API_KEY=YOUR_NFT_STORAGE_API_KEY_HERE
   DEBUG=True
   ```
5. Start the FastAPI server:
   ```
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup
1. Open `index.html` in a browser (you can use Python's built-in HTTP server):
   ```
   cd frontend
   python -m http.server
   ```
   Or use VSCode Live Server extension

### Blockchain Setup (Automated)

We've created a setup script to help you configure the blockchain integration:

1. Install Node.js if you haven't already
2. Install the Aptos CLI: https://aptos.dev/tools/aptos-cli/
3. Run the setup script:
   ```
   node setup-blockchain.js
   ```
4. Follow the prompts to:
   - Create a new Aptos account
   - Fund it with testnet tokens
   - Deploy the smart contract
   - Configure your NFT.Storage API key (optional)

### Blockchain Setup (Manual)

If you prefer to set up manually:

1. Install the Aptos CLI: https://aptos.dev/tools/aptos-cli/
2. Create a new Aptos account:
   ```
   aptos init --profile plagiarism-checker --network testnet
   ```
3. Fund your account with testnet tokens from the [Aptos Faucet](https://aptoslabs.com/testnet-faucet)
4. Deploy the contract:
   ```
   cd contracts
   aptos move publish --named-addresses AcademicNFT=YOUR_ACCOUNT_ADDRESS --profile plagiarism-checker
   ```
5. Update your `.env` file with your account address and private key

### Wallet Setup

1. Install the [Petra](https://petra.app/) or [Martian](https://martianwallet.xyz/) wallet extension
2. Create a new wallet or import an existing one
3. Switch to the Aptos testnet
4. Get testnet tokens from the [Aptos Faucet](https://aptoslabs.com/testnet-faucet)

## 🧪 Using the Application

### As a Student:
1. Open `index.html` in your browser
2. Connect your wallet using the "Connect Wallet" button
3. Enter a title for your document and upload your file (PDF, DOCX, or TXT)
4. Click "Analyze Document" to check for plagiarism
5. Review the plagiarism score and AI-generated summary
6. Click "Mint as NFT" to create an NFT of your work on the Aptos blockchain

### As a Teacher:
1. Open `teacher.html` in your browser
2. Connect your wallet using the "Connect Wallet" button
3. View the list of student submissions
4. Click on a submission to see details and provide feedback

## 📚 IPFS & NFT Storage

This project uses a mock IPFS implementation by default. To use NFT.Storage:

1. Create an account at [nft.storage](https://nft.storage/)
2. Generate an API key
3. Add the API key to your `.env` file
4. Modify the `ipfs_upload.py` file to use the NFT.Storage API

## 🔗 Aptos Blockchain Integration

The project uses the Aptos blockchain for minting NFTs. The Move smart contract handles the creation and management of academic NFTs.

To interact with the Aptos blockchain:
1. Install the Petra or Martian wallet browser extension
2. Create or import a wallet
3. Switch to the Aptos testnet
4. Get testnet tokens from the [Aptos Faucet](https://aptoslabs.com/testnet-faucet)

## 📄 License

MIT