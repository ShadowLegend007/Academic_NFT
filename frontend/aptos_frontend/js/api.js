// API Configuration
const API_BASE_URL = 'http://localhost:8000'; // Update this to match your backend URL

// Firebase Configuration - Replace with your actual Firebase config
const FIREBASE_CONFIG = {
    apiKey: "AIzaSyDt6-CBaHRXo8BkNCUjVOSfg8gJt8tSbH8",
    authDomain: "magistics-ee00c.firebaseapp.com",
    projectId: "magistics-ee00c",
    storageBucket: "magistics-ee00c.firebasestorage.app",
    messagingSenderId: "501298222547",
    appId: "1:501298222547:web:4ef296553d086cef6b8b26",
    measurementId: "G-NQZE101W1W"
};

// Initialize Firebase if it's not already initialized
try {
    if (typeof firebase !== 'undefined') {
        // Initialize Firebase if not already initialized
        if (!firebase.apps || !firebase.apps.length) {
            console.log("Initializing Firebase with config:", FIREBASE_CONFIG);
            firebase.initializeApp(FIREBASE_CONFIG);
        } else {
            console.log("Firebase already initialized");
        }
    } else {
        console.error("Firebase SDK not loaded");
        initMockFirebase();
    }
} catch (error) {
    console.error("Error initializing Firebase:", error);
    initMockFirebase();
}

// Initialize mock Firebase for development/fallback
function initMockFirebase() {
    console.log("Loading mock Firebase implementation.");
    // Mock Firebase implementation for development
    window.firebase = {
        auth: () => ({
            createUserWithEmailAndPassword: async (email, password) => {
                console.log(`Mock Firebase: Creating user with email ${email}`);
                return { 
                    user: { 
                        uid: `mock_uid_${Date.now()}`,
                        email: email
                    } 
                };
            },
            signInWithEmailAndPassword: async (email, password) => {
                console.log(`Mock Firebase: Signing in user with email ${email}`);
                return { 
                    user: { 
                        uid: `mock_uid_${Date.now()}`,
                        email: email
                    } 
                };
            }
        }),
        firestore: () => ({
            collection: (name) => ({
                doc: (id) => ({
                    set: async (data) => {
                        console.log(`Mock Firebase: Setting document ${id} in collection ${name}:`, data);
                        return Promise.resolve();
                    },
                    get: async () => {
                        console.log(`Mock Firebase: Getting document ${id} from collection ${name}`);
                        return {
                            exists: true,
                            data: () => ({ 
                                name: 'Mock User',
                                email: 'mock@example.com',
                                role: 'student'
                            })
                        };
                    }
                })
            })
        }),
        storage: () => ({
            ref: (path) => ({
                put: async (file) => {
                    console.log(`Mock Firebase: Uploading file to ${path}:`, file);
                    return {
                        ref: {
                            getDownloadURL: async () => `https://mock-storage-url.com/${path}`
                        }
                    };
                }
            })
        })
    };
}

// API Service Class
class APIService {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.firebase = window.firebase;
    }

    // Firebase user registration
    async registerUser(userData) {
        try {
            console.log("Registering user with Firebase:", userData.email);
            
            // Create user in Firebase Authentication
            const authResult = await this.firebase.auth().createUserWithEmailAndPassword(
                userData.email, 
                userData.password
            );
            
            const uid = authResult.user.uid;
            console.log("User created with UID:", uid);
            
            // Upload verification document if provided
            let verificationDocUrl = null;
            if (userData.verificationDoc) {
                console.log("Uploading verification document");
                const storageRef = this.firebase.storage().ref(`verification_docs/${uid}`);
                const uploadTask = await storageRef.put(userData.verificationDoc);
                verificationDocUrl = await uploadTask.ref.getDownloadURL();
                console.log("Document uploaded:", verificationDocUrl);
            }
            
            // Save user data to Firestore
            const userDocData = {
                uid: uid,
                email: userData.email,
                name: userData.fullName,
                role: userData.role === 'teacher' ? 'pending_teacher' : 'student',
                createdAt: new Date().toISOString(),
                verificationDocUrl: verificationDocUrl,
                verificationStatus: userData.role === 'teacher' ? 'pending' : null
            };
            
            await this.firebase.firestore().collection('users').doc(uid).set(userDocData);
            console.log("User data saved to Firestore");
            
            return {
                uid,
                ...userDocData
            };
        } catch (error) {
            console.error("Firebase registration error:", error);
            throw new Error(error.message || 'Registration failed');
        }
    }

    // Firebase user login
    async loginUser(email, password) {
        try {
            console.log("Logging in with Firebase:", email);
            
            const authResult = await this.firebase.auth().signInWithEmailAndPassword(
                email, 
                password
            );
            
            const uid = authResult.user.uid;
            console.log("User logged in with UID:", uid);
            
            // Get user data from Firestore
            const userDoc = await this.firebase.firestore().collection('users').doc(uid).get();
            
            if (!userDoc.exists) {
                throw new Error('User data not found');
            }
            
            const userData = userDoc.data();
            console.log("User data retrieved from Firestore:", userData);
            
            return {
                uid,
                ...userData
            };
        } catch (error) {
            console.error("Firebase login error:", error);
            throw new Error(error.message || 'Login failed');
        }
    }

    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            console.log(`Making request to: ${url}`, config);
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error(`HTTP error! status: ${response.status}, response: ${errorText}`);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log(`Response from ${url}:`, data);
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                throw new Error('Network error: Unable to connect to the server. Please check if the backend is running.');
            }
            throw error;
        }
    }

    // File upload
    async uploadFile(file, title, authToken) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', title);

        try {
            console.log(`Uploading file: ${file.name} with title: ${title}`);
            const response = await fetch(`${this.baseURL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Upload failed: ${errorData.error || response.status}`);
            }

            const data = await response.json();
            console.log('Upload response:', data);
            return data;
        } catch (error) {
            console.error('Upload failed:', error);
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                throw new Error('Network error: Unable to connect to the server. Please check if the backend is running.');
            }
            throw error;
        }
    }

    // Analyze file
    async analyzeFile(fileId, authToken) {
        console.log(`Analyzing file with ID: ${fileId}`);
        try {
            const result = await this.request('/analyze', {
                method: 'POST',
                body: JSON.stringify({ file_id: fileId })
            });
            console.log(`Analysis result:`, result);
            return result;
        } catch (error) {
            console.error(`Analysis failed: ${error.message}`);
            throw error;
        }
    }

    // Mint NFT
    async mintNFT(mintData, authToken) {
        console.log(`Minting NFT with data:`, mintData);
        try {
            const result = await this.request('/mint', {
                method: 'POST',
                body: JSON.stringify(mintData)
            });
            console.log(`Mint result:`, result);
            return result;
        } catch (error) {
            console.error(`Minting failed: ${error.message}`);
            throw error;
        }
    }

    // Get NFTs
    async getNFTs(authToken = null) {
        return await this.request('/nfts', {});
    }

    // Submit feedback
    async submitFeedback(feedbackData) {
        return await this.request('/feedback', {
            method: 'POST',
            body: JSON.stringify(feedbackData)
        });
    }

    // Teacher comment
    async submitTeacherComment(commentData, authToken) {
        return await this.request('/teacher/comment', {
            method: 'POST',
            body: JSON.stringify(commentData)
        });
    }

    // Check API health
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/`);
            return response.ok;
        } catch (error) {
            console.error('API health check failed:', error);
            return false;
        }
    }
}

// Create global API instance
window.apiService = new APIService();

// Utility functions for common API operations
window.APIUtils = {
    // Handle file upload with progress
    async uploadWithProgress(file, title, authToken, onProgress) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', title);

        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    onProgress(percentComplete);
                }
            });

            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    resolve(JSON.parse(xhr.responseText));
                } else {
                    reject(new Error(`Upload failed: ${xhr.status}`));
                }
            });

            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });

            xhr.open('POST', `${API_BASE_URL}/upload`);
            xhr.setRequestHeader('Authorization', `Bearer ${authToken}`);
            xhr.send(formData);
        });
    },

    // Format file size
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Validate file type
    validateFileType(file) {
        const allowedTypes = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword',
            'text/plain'
        ];
        return allowedTypes.includes(file.type);
    },

    // Get file extension
    getFileExtension(filename) {
        return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
    },

    // Show API error message
    showError(message, duration = 5000) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);

        setTimeout(() => {
            errorDiv.remove();
        }, duration);
    },

    // Show success message
    showSuccess(message, duration = 3000) {
        const successDiv = document.createElement('div');
        successDiv.className = 'fixed top-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        successDiv.textContent = message;
        document.body.appendChild(successDiv);

        setTimeout(() => {
            successDiv.remove();
        }, duration);
    }
}; 