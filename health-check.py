#!/usr/bin/env python3
import requests
import time
import sys

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running (Connection refused)")
        return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running (Connection refused)")
        return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API endpoints...")
    
    # Test NFTs endpoint
    try:
        response = requests.get('http://localhost:8000/nfts', timeout=5)
        if response.status_code == 200:
            nfts = response.json()
            print(f"✅ NFTs endpoint: {len(nfts)} NFTs found")
        else:
            print(f"❌ NFTs endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ NFTs endpoint error: {e}")
    
    # Test upload endpoint (without actually uploading)
    try:
        response = requests.post('http://localhost:8000/upload', timeout=5)
        # Should return 400 for missing file, which is expected
        if response.status_code == 400:
            print("✅ Upload endpoint is accessible")
        else:
            print(f"⚠️ Upload endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload endpoint error: {e}")

def main():
    print("🏥 Academic NFT Health Check")
    print("=" * 40)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    if backend_ok and frontend_ok:
        print("\n🎉 All systems are running!")
        test_api_endpoints()
        print("\n📋 Next steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Test the application at http://localhost:3000/test-api.html")
        print("3. Upload a document at http://localhost:3000/student_upload.html")
    else:
        print("\n⚠️ Some services are not running:")
        if not backend_ok:
            print("- Backend server needs to be started")
            print("  Run: cd backend && python main.py")
        if not frontend_ok:
            print("- Frontend server needs to be started")
            print("  Run: cd frontend/aptos_frontend && python -m http.server 3000")
        
        print("\n💡 Quick start:")
        print("  Run: start-all.bat (Windows) or ./start-all.sh (Unix)")

if __name__ == "__main__":
    main() 