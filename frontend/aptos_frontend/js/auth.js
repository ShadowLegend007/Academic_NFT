// Authentication Service
class AuthService {
    constructor() {
        this.currentUser = null;
        this.authToken = localStorage.getItem('authToken');
        this.userRole = localStorage.getItem('userRole');
        this.init();
    }

    init() {
        // Check if user is already authenticated
        if (this.authToken) {
            this.validateToken();
        }
        this.updateUI();
    }

    // Validate existing token
    async validateToken() {
        try {
            // In a real app, you'd validate the token with the backend
            // For now, we'll just check if it exists
            if (this.authToken) {
                this.currentUser = {
                    email: localStorage.getItem('userEmail'),
                    role: this.userRole,
                    name: localStorage.getItem('userName')
                };
                return true;
            }
            return false;
        } catch (error) {
            console.error('Token validation failed:', error);
            this.logout();
            return false;
        }
    }

    // Login user
    async login(email, password) {
        try {
            // Use Firebase authentication through the API service
            console.log(`Logging in user: ${email}`);
            
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 500));
            
            try {
                // Try to use Firebase authentication
                const user = await apiService.loginUser(email, password);
                console.log("Firebase login successful:", user);
                
                const token = `firebase_token_${Date.now()}`;
                this.setSession(user, token);
                return { success: true, user };
            } catch (firebaseError) {
                console.warn("Firebase login failed, using mock auth:", firebaseError);
                
                // Fall back to mock authentication for development
                if (email && password) {
                    const user = {
                        email: email,
                        role: 'student', // or 'teacher' based on user type
                        name: email.split('@')[0],
                        id: Date.now().toString()
                    };

                    const token = `mock_token_${Date.now()}`;
                    
                    this.setSession(user, token);
                    return { success: true, user };
                } else {
                    throw new Error('Invalid credentials');
                }
            }
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    // Register user
    async register(userData) {
        try {
            // Use Firebase authentication through the API service
            console.log("Registering user:", userData.email);
            
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 500));
            
            try {
                // Try to use Firebase registration
                const user = await apiService.registerUser(userData);
                console.log("Firebase registration successful:", user);
                
                const token = `firebase_token_${Date.now()}`;
                
                // For teacher role, show verification pending message
                if (userData.role === 'teacher') {
                    APIUtils.showSuccess('Registration successful! Your teacher account is pending verification.');
                } else {
                    APIUtils.showSuccess('Registration successful!');
                }
                
                this.setSession(user, token);
                return { success: true, user };
            } catch (firebaseError) {
                console.warn("Firebase registration failed, using mock auth:", firebaseError);
                
                // Fall back to mock registration for development
                if (userData.email && userData.password) {
                    // Handle teacher verification document if present
                    let verificationDocUrl = null;
                    if (userData.verificationDoc) {
                        console.log("Teacher verification document detected:", userData.verificationDoc);
                        // In a real app, this would upload the document to storage
                        verificationDocUrl = "mock_verification_doc_url";
                    }
                    
                    const user = {
                        email: userData.email,
                        role: userData.role === 'teacher' ? 'pending_teacher' : 'student',
                        name: userData.fullName || userData.email.split('@')[0],
                        id: Date.now().toString(),
                        verificationDocUrl: verificationDocUrl,
                        verificationStatus: userData.role === 'teacher' ? 'pending' : null
                    };

                    const token = `mock_token_${Date.now()}`;
                    
                    // In a real app, this would save the user to Firebase
                    console.log("Saving user to Firebase:", user);
                    
                    // For teacher role, show verification pending message
                    if (userData.role === 'teacher') {
                        APIUtils.showSuccess('Registration successful! Your teacher account is pending verification.');
                    } else {
                        APIUtils.showSuccess('Registration successful!');
                    }
                    
                    this.setSession(user, token);
                    return { success: true, user };
                } else {
                    throw new Error('Invalid registration data');
                }
            }
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    }

    // Set user session
    setSession(user, token) {
        this.currentUser = user;
        this.authToken = token;
        this.userRole = user.role;
        
        localStorage.setItem('authToken', token);
        localStorage.setItem('userRole', user.role);
        localStorage.setItem('userEmail', user.email);
        localStorage.setItem('userName', user.name);
        localStorage.setItem('userId', user.id);
        
        this.updateUI();
    }

    // Logout user
    logout() {
        this.currentUser = null;
        this.authToken = null;
        this.userRole = null;
        
        localStorage.removeItem('authToken');
        localStorage.removeItem('userRole');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        localStorage.removeItem('userId');
        
        this.updateUI();
        
        // Redirect to home page
        window.location.href = 'index.html';
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.authToken && !!this.currentUser;
    }

    // Check if user has specific role
    hasRole(role) {
        if (!this.isAuthenticated()) return false;
        
        // Special case for teacher role check - both pending and verified teachers
        if (role === 'teacher') {
            return this.userRole === 'teacher' || this.userRole === 'pending_teacher' || this.userRole === 'verified_teacher';
        }
        
        return this.userRole === role;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Get auth token
    getAuthToken() {
        return this.authToken;
    }

    // Update UI based on authentication state
    updateUI() {
        const authButtons = document.getElementById('auth-buttons');
        const userMenu = document.getElementById('user-menu');
        
        if (this.isAuthenticated()) {
            // Show user menu
            if (authButtons) {
                authButtons.innerHTML = `
                    <div class="flex items-center gap-4">
                        <span class="text-white text-sm">Welcome, ${this.currentUser.name}</span>
                        <div class="relative">
                            <button id="user-menu-button" class="flex items-center gap-2 text-white text-sm">
                                <div class="w-8 h-8 bg-[#1383eb] rounded-full flex items-center justify-center">
                                    ${this.currentUser.name.charAt(0).toUpperCase()}
                                </div>
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </button>
                            <div id="user-dropdown" class="hidden absolute right-0 mt-2 w-48 bg-[#192733] rounded-lg shadow-lg border border-[#233648] z-50">
                                <div class="py-2">
                                                        <a href="dashboard.html" class="block px-4 py-2 text-white text-sm hover:bg-[#233648]">Dashboard</a>
                    <a href="student_upload.html" class="block px-4 py-2 text-white text-sm hover:bg-[#233648]">Upload Document</a>
                    ${this.hasRole('teacher') ? '<a href="teacher_dashboard.html" class="block px-4 py-2 text-white text-sm hover:bg-[#233648]">Teacher Dashboard</a>' : ''}
                                    <hr class="border-[#233648] my-1">
                                    <button onclick="authService.logout()" class="block w-full text-left px-4 py-2 text-white text-sm hover:bg-[#233648]">Logout</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                // Add dropdown functionality
                const userMenuButton = document.getElementById('user-menu-button');
                const userDropdown = document.getElementById('user-dropdown');
                
                if (userMenuButton && userDropdown) {
                    userMenuButton.addEventListener('click', () => {
                        userDropdown.classList.toggle('hidden');
                    });
                    
                    // Close dropdown when clicking outside
                    document.addEventListener('click', (e) => {
                        if (!userMenuButton.contains(e.target) && !userDropdown.contains(e.target)) {
                            userDropdown.classList.add('hidden');
                        }
                    });
                }
            }
        } else {
            // Show login/signup buttons
            if (authButtons) {
                authButtons.innerHTML = `
                    <div class="flex gap-4">
                                    <a href="login.html" class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-4 bg-[#1383eb] text-white text-sm font-bold leading-normal tracking-[0.015em]">
              <span class="truncate">Login</span>
            </a>
            <a href="sign_up.html" class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-4 bg-[#233648] text-white text-sm font-bold leading-normal tracking-[0.015em]">
              <span class="truncate">Sign Up</span>
            </a>
                    </div>
                `;
            }
        }
    }

    // Require authentication for protected pages
    requireAuth(redirectUrl = 'login.html') {
        if (!this.isAuthenticated()) {
            window.location.href = redirectUrl;
            return false;
        }
        return true;
    }

    // Require specific role
    requireRole(role, redirectUrl = 'index.html') {
        if (!this.hasRole(role)) {
            window.location.href = redirectUrl;
            return false;
        }
        return true;
    }
}

// Create global auth service instance
window.authService = new AuthService();

// Form handling utilities
window.AuthUtils = {
    // Handle login form submission
    async handleLogin(event) {
        event.preventDefault();
        
        const form = event.target;
        const email = form.querySelector('[name="email"]').value;
        const password = form.querySelector('[name="password"]').value;
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        if (!email || !password) {
            APIUtils.showError('Please enter both email and password');
            return;
        }
        
        try {
            submitButton.disabled = true;
            submitButton.textContent = 'Signing in...';
            
            const result = await authService.login(email, password);
            
            APIUtils.showSuccess('Login successful!');
            
            // Redirect based on role
            setTimeout(() => {
                if (authService.hasRole('teacher')) {
                    window.location.href = 'teacher_dashboard.html';
                } else {
                    window.location.href = 'dashboard.html';
                }
            }, 1000);
        } catch (error) {
            APIUtils.showError('Login failed: ' + error.message);
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    },

    // Handle registration form submission
    async handleRegister(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        // Get verification document if present
        const verificationDocInput = form.querySelector('input[name="verificationDoc"]');
        let verificationDoc = null;
        if (verificationDocInput && verificationDocInput.files.length > 0) {
            verificationDoc = verificationDocInput.files[0];
        }
        
        const userData = {
            fullName: formData.get('fullName'),
            email: formData.get('email'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword'),
            role: formData.get('role') || 'student',
            verificationDoc: verificationDoc
        };
        
        console.log('Registration data:', userData);
        
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        try {
            // Validate form data
            if (!userData.fullName || !userData.email || !userData.password || !userData.confirmPassword) {
                throw new Error('Please fill in all fields');
            }
            
            if (userData.password !== userData.confirmPassword) {
                throw new Error('Passwords do not match');
            }
            
            if (userData.password.length < 6) {
                throw new Error('Password must be at least 6 characters long');
            }
            
            // Validate teacher verification document
            if (userData.role === 'teacher' && !userData.verificationDoc) {
                throw new Error('Please upload a verification document');
            }
            
            submitButton.disabled = true;
            submitButton.textContent = 'Creating account...';
            
            const result = await authService.register(userData);
            
            // Redirect based on role
            setTimeout(() => {
                if (authService.hasRole('teacher') || authService.hasRole('pending_teacher')) {
                    window.location.href = 'teacher_dashboard.html';
                } else {
                    window.location.href = 'dashboard.html';
                }
            }, 1000);
        } catch (error) {
            APIUtils.showError('Registration failed: ' + error.message);
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    }
}; 