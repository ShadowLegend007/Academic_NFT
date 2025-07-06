# Decentralized Academic Plagiarism Checker

A decentralized web application that allows students to check their academic papers for plagiarism, get AI-generated summaries, and mint their work as NFTs on the Aptos blockchain. Features secure Firebase authentication with teacher/student role verification.

## 🔐 Authentication & Authorization

This application now includes **Firebase Authentication** with role-based access control:

- **Students**: Can upload documents, check plagiarism, and mint NFTs
- **Teachers**: Can review submissions and provide feedback (after admin approval)
- **Admins**: Can approve teacher applications and manage the system

### User Roles:
- `student`: Can use all student features
- `pending_teacher`: Teacher awaiting admin approval
- `verified_teacher`: Approved teacher with access to dashboard
- `admin`: System administrator with approval privileges

## 🔧 Tech Stack

### Frontend
- HTML + Bootstrap + Vanilla JavaScript
- Firebase Authentication & Firestore
- Aptos Wallet Adapter for wallet connection
- Tailwind CSS for styling

### Backend
- Python FastAPI
- Firebase Admin SDK for authentication
- Enhanced plagiarism detection with multiple algorithms:
  - Cosine Similarity
  - TF-IDF (Term Frequency-Inverse Document Frequency)
  - N-Gram analysis
  - Comprehensive weighted scoring
- HuggingFace T5/Pegasus for text summarization

### Storage
- Firebase Firestore for user data
- Firebase Storage for teacher verification documents
- IPFS via mock implementation (can be upgraded to nft.storage)

### Blockchain
- Aptos Move smart contract for NFT minting
- Petra/Martian Wallet integration

## 📂 Project Structure

```
/frontend
├── landing.html            # Home page with login/signup options
├── index.html              # Student dashboard
├── login.html              # Login page
├── signup.html             # Signup page with role selection
├── pending.html            # Teacher pending approval page
├── dashboard.html          # Teacher dashboard
├── admin.html              # Admin approval dashboard
├── teacher.html            # Legacy teacher page
├── styles.css
├── app.js
└── js/
    └── firebase.js         # Firebase configuration

/backend
├── main.py
├── routes/
│   ├── upload.py
│   ├── analyze.py
│   └── mint.py
├── utils/
│   ├── firebase_auth.py    # Firebase authentication middleware
│   ├── plagiarism_check.py
│   ├── plagiarism_algorithms.py
│   ├── summarizer.py
│   └── ipfs_upload.py
├── corpus/
└── models/

/contracts
└── AcademicNFT.move

.env.example
README.md
FIREBASE_SETUP.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for blockchain setup)
- Aptos CLI
- Google account (for Firebase)
- Petra or Martian wallet browser extension

### 1. Clone and Setup
```bash
git clone <repository-url>
cd plagarism-checker
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Firebase Setup (Required)
Follow the detailed Firebase setup guide below, or use the quick setup:

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Authentication (Email/Password)
3. Create Firestore Database
4. Create Storage bucket
5. Get your Firebase config and update `frontend/js/firebase.js`
6. Download service account key and save as `firebase-service-account.json`

### 4. Environment Configuration
Create a `.env` file:
```env
APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1
APTOS_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS_HERE
NFT_STORAGE_API_KEY=YOUR_NFT_STORAGE_API_KEY_HERE
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
DEBUG=True
```

### 5. Start the Application
```bash
# Start backend
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (in another terminal)
cd frontend
python -m http.server 8080
```

### 6. Access the Application
- Open `http://localhost:8080` in your browser
- Sign up as a student or teacher
- Connect your wallet to use blockchain features

## 🔥 Firebase Authentication Setup (Detailed)

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Enter project name (e.g., "academic-plagiarism-checker")
4. Enable Google Analytics (optional)
5. Click "Create project"

### Step 2: Enable Authentication
1. Go to "Authentication" → "Sign-in method"
2. Enable "Email/Password" authentication
3. Click "Save"

### Step 3: Set up Firestore Database
1. Go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location
5. Click "Done"

### Step 4: Set up Firebase Storage
1. Go to "Storage"
2. Click "Get started"
3. Choose "Start in test mode" (for development)
4. Select a location
5. Click "Done"

### Step 5: Configure Security Rules

**Firestore Rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Only admins can update user roles
    match /users/{userId} {
      allow update: if request.auth != null && 
        (request.auth.uid == userId || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin');
    }
  }
}
```

**Storage Rules:**
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Users can read/write their own proof files
    match /teacher-proofs/{userId}/{fileName} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### Step 6: Get Firebase Configuration
1. Go to "Project settings" → "Your apps"
2. Click "Add app" → "Web"
3. Register your app
4. Copy the Firebase configuration object

### Step 7: Update Frontend Configuration
The Firebase configuration is already set up in `frontend/js/firebase.js` for the "magistics-ee00c" project:

```javascript
const firebaseConfig = {
    apiKey: "AIzaSyDt6-CBaHRXo8BkNCUjVOSfg8gJt8tSbH8",
    authDomain: "magistics-ee00c.firebaseapp.com",
    projectId: "magistics-ee00c",
    storageBucket: "magistics-ee00c.firebasestorage.app",
    messagingSenderId: "501298222547",
    appId: "1:501298222547:web:4ef296553d086cef6b8b26",
    measurementId: "G-NQZE101W1W"
};
```

### Step 8: Set up Backend Firebase Admin SDK
1. Go to "Project settings" → "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. Save as `firebase-service-account.json` in project root
5. Add to `.env`:
```env
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
```

### Step 9: Create Admin User
1. Sign up a new user through the application
2. In Firebase Console, go to "Firestore Database"
3. Find the user document in `users` collection
4. Manually update the role to `admin`:
```json
{
  "displayName": "Admin User",
  "email": "admin@academicplagiarism.com",
  "role": "admin",
  "createdAt": "timestamp"
}
```

## 🧪 User Flow Testing

### Student Flow:
1. Go to `signup.html`
2. Select "Student" role
3. Fill in details and sign up
4. Redirected to `index.html`
5. Can upload documents and mint NFTs

### Teacher Flow:
1. Go to `signup.html`
2. Select "Teacher" role
3. Upload verification document
4. Redirected to `pending.html`
5. Admin approves in `admin.html`
6. Teacher can access `dashboard.html`

### Admin Flow:
1. Sign in as admin user
2. Go to `admin.html`
3. Review pending teacher applications
4. Approve teachers by clicking "Approve"

## 🔗 Blockchain Setup

### Automated Setup
```bash
node setup-blockchain.js
```

### Manual Setup
1. Install Aptos CLI: https://aptos.dev/tools/aptos-cli/
2. Create account:
```bash
aptos init --profile plagiarism-checker --network testnet
```
3. Fund account from [Aptos Faucet](https://aptoslabs.com/testnet-faucet)
4. Deploy contract:
```bash
cd contracts
aptos move publish --named-addresses AcademicNFT=YOUR_ACCOUNT_ADDRESS --profile plagiarism-checker
```

### Wallet Setup
1. Install [Petra](https://petra.app/) or [Martian](https://martianwallet.xyz/)
2. Create/import wallet
3. Switch to Aptos testnet
4. Get testnet tokens from [Aptos Faucet](https://aptoslabs.com/testnet-faucet)

## 📚 API Endpoints

### Authentication Required Endpoints:
- `POST /upload` - Upload document (student role required)
- `POST /analyze` - Analyze document (student role required)
- `POST /mint` - Mint NFT (student role required)
- `GET /nfts` - Get all NFTs (optional auth)
- `POST /teacher/comment` - Submit teacher feedback (verified teacher role required)

### Enhanced Analysis Endpoints:
- `POST /api/v1/analyze-text` - Analyze text for plagiarism
- `POST /api/v1/compare-texts` - Compare two texts directly
- `POST /api/v1/analyze-detailed` - Configurable analysis with algorithm selection
- `GET /api/v1/corpus-info` - Get information about reference corpus

## 🔒 Security Considerations

1. **Environment Variables**: Never commit Firebase credentials to version control
2. **CORS**: Configure CORS properly for production
3. **Rate Limiting**: Implement rate limiting for authentication endpoints
4. **Input Validation**: Validate all user inputs
5. **HTTPS**: Use HTTPS in production
6. **Firebase Security Rules**: Configure proper Firestore and Storage rules

## 🐛 Troubleshooting

### Common Issues:

1. **"Firebase app already initialized"**
   - This is normal if the app is already initialized
   - The error is caught and ignored

2. **"Permission denied" errors**
   - Check Firestore security rules
   - Ensure user is authenticated
   - Verify user has correct role

3. **"Invalid API key"**
   - Check Firebase configuration
   - Ensure API key is correct
   - Verify project settings

4. **"User not found in database"**
   - Check if user document exists in Firestore
   - Verify user creation process

### Debug Mode:
Enable debug logging in browser console:
```javascript
localStorage.setItem('debug', 'firebase:*');
```

## 📱 Using the Application

### As a Student:
1. Open `index.html` in your browser
2. Sign up/login with Firebase authentication
3. Connect your wallet using the "Connect Wallet" button
4. Enter a title for your document and upload your file (PDF, DOCX, or TXT)
5. Click "Analyze Document" to check for plagiarism using enhanced algorithms
6. Review the comprehensive plagiarism analysis and AI-generated summary
7. Click "Mint as NFT" to create an NFT of your work on the Aptos blockchain

### As a Teacher:
1. Sign up as a teacher and wait for admin approval
2. Once approved, access `dashboard.html`
3. View the list of student submissions
4. Click on a submission to see details and provide feedback

### As an Admin:
1. Sign in as admin user
2. Access `admin.html`
3. Review pending teacher applications
4. Approve teachers by clicking "Approve"

## 📚 IPFS & NFT Storage

This project uses a mock IPFS implementation by default. To use NFT.Storage:

1. Create an account at [nft.storage](https://nft.storage/)
2. Generate an API key
3. Add the API key to your `.env` file
4. Modify the `ipfs_upload.py` file to use the NFT.Storage API

## 🎯 Next Steps

1. **Production Deployment**: Set up proper hosting and domain
2. **Email Verification**: Enable email verification for users
3. **Password Reset**: Implement password reset functionality
4. **Social Login**: Add Google, GitHub, or other social login options
5. **Analytics**: Set up Firebase Analytics for user behavior tracking
6. **Monitoring**: Set up Firebase Performance Monitoring

## 📚 Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Auth Guide](https://firebase.google.com/docs/auth)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Firebase Storage Rules](https://firebase.google.com/docs/storage/security)
- [Aptos Documentation](https://aptos.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📞 Support

If you encounter issues:
1. Check the Firebase Console for error logs
2. Review browser console for JavaScript errors
3. Check backend logs for Python errors
4. Verify all configuration steps are completed

## 📄 License

MIT

---

**Happy coding! 🚀**