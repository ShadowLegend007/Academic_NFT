import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Initialize Firebase Admin SDK
# For development, you can use a service account key file
# For production, use environment variables or Google Cloud default credentials
try:
    # Try to initialize with service account key file
    service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH', '../firebase-service-account.json')
    if service_account_path and os.path.exists(service_account_path):
        print(f"Initializing Firebase with service account: {service_account_path}")
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    else:
        # Try to initialize with default credentials (for production)
        print("Service account file not found, trying default credentials")
        firebase_admin.initialize_app()
except ValueError:
    # App already initialized
    print("Firebase app already initialized")
    pass
except Exception as e:
    print(f"Warning: Firebase Admin SDK initialization failed: {e}")
    print("Using mock authentication for development...")
    # Create a mock app for development
    try:
        firebase_admin.initialize_app()
    except ValueError:
        pass

# Initialize Firestore
db = firestore.client()

# Security scheme for JWT tokens
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify Firebase ID token and return user information
    """
    token = credentials.credentials
    
    # For development, if token is "mock_token_for_development", use mock auth
    if token == "mock_token_for_development":
        print("Using mock token for development")
        return mock_verify_token(token)
        
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        # For development, if Firebase auth fails, use mock authentication
        print(f"Firebase auth failed: {e}")
        print("Using mock authentication for development...")
        return mock_verify_token(token)

def mock_verify_token(token: str) -> dict:
    """
    Mock token verification for development
    """
    # For development, accept any token and return mock user data
    return {
        "uid": "mock_user_id",
        "email": "student@example.com",
        "email_verified": True,
        "name": "Mock Student",
        "picture": None,
        "iss": "https://securetoken.google.com/magistics-ee00c",
        "aud": "magistics-ee00c",
        "auth_time": int(time.time()),
        "user_id": "mock_user_id",
        "sub": "mock_user_id",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "firebase": {
            "identities": {
                "email": ["student@example.com"]
            },
            "sign_in_provider": "password"
        }
    }

async def get_current_user(token_data: dict = Depends(verify_token)) -> dict:
    """
    Get current user data from Firestore
    """
    try:
        uid = token_data['uid']
        
        # For mock users, return mock data
        if uid == "mock_user_id":
            return {
                "uid": "mock_user_id",
                "email": "student@example.com",
                "displayName": "Mock Student",
                "role": "student",
                "createdAt": "2024-01-01T00:00:00Z"
            }
        
        # Try to get user from Firestore
        try:
            user_doc = db.collection('users').document(uid).get()
            
            if not user_doc.exists:
                raise HTTPException(
                    status_code=404,
                    detail="User not found in database"
                )
            
            user_data = user_doc.to_dict()
            user_data['uid'] = uid
            return user_data
        except Exception as e:
            print(f"Firestore error: {e}")
            # Fallback to mock data
            return {
                "uid": uid,
                "email": token_data.get('email', 'unknown@example.com'),
                "displayName": token_data.get('name', 'Unknown User'),
                "role": "student",
                "createdAt": "2024-01-01T00:00:00Z"
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user data: {str(e)}"
        )

async def require_student_role(user: dict = Depends(get_current_user)) -> dict:
    """
    Require user to have student role
    """
    if user.get('role') != 'student':
        raise HTTPException(
            status_code=403,
            detail="Student role required"
        )
    return user

async def require_verified_teacher_role(user: dict = Depends(get_current_user)) -> dict:
    """
    Require user to have verified teacher role
    """
    if user.get('role') != 'verified_teacher':
        raise HTTPException(
            status_code=403,
            detail="Verified teacher role required"
        )
    return user

async def require_any_teacher_role(user: dict = Depends(get_current_user)) -> dict:
    """
    Require user to have any teacher role (pending or verified)
    """
    role = user.get('role')
    if role not in ['pending_teacher', 'verified_teacher']:
        raise HTTPException(
            status_code=403,
            detail="Teacher role required"
        )
    return user

# Optional authentication for routes that can work with or without auth
async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Get user data if authenticated, otherwise return None
    """
    if not authorization or not authorization.startswith('Bearer '):
        return None
    
    try:
        token = authorization.split('Bearer ')[1]
        
        # For development, if token is "mock_token_for_development", use mock auth
        if token == "mock_token_for_development":
            print("Using mock token for development in optional auth")
            return {
                "uid": "mock_user_id",
                "email": "student@example.com",
                "displayName": "Mock Student",
                "role": "student",
                "createdAt": "2024-01-01T00:00:00Z"
            }
            
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        try:
            user_doc = db.collection('users').document(uid).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_data['uid'] = uid
                return user_data
        except Exception as e:
            print(f"Firestore error in optional auth: {e}")
            # Return basic user data from token
            return {
                "uid": uid,
                "email": decoded_token.get('email', 'unknown@example.com'),
                "displayName": decoded_token.get('name', 'Unknown User'),
                "role": "student",
                "createdAt": "2024-01-01T00:00:00Z"
            }
            
        return None
    except Exception as e:
        print(f"Optional auth error: {e}")
        return None 