// Main Application Controller
class AcademicNFTApp {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.init();
    }

    init() {
        console.log('Academic NFT App initialized');
        
        // Initialize authentication
        this.initAuth();
        
        // Initialize page-specific functionality
        this.initPageHandlers();
        
        // Check API health
        this.checkAPIHealth();
        
        // Set up global event listeners
        this.setupGlobalListeners();
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('login.html')) return 'login';
        if (path.includes('sign_up.html')) return 'signup';
        if (path.includes('student_upload.html')) return 'student-upload';
        if (path.includes('teacher_dashboard.html')) return 'teacher-dashboard';
        if (path.includes('teacher_signup.html')) return 'teacher-signup';
        if (path.includes('dashboard.html')) return 'dashboard';
        if (path.includes('about_us.html')) return 'about';
        if (path.includes('contact_us.html')) return 'contact';
        if (path.includes('get_started.html')) return 'get-started';
        if (path.includes('home.html')) return 'home';
        return 'index';
    }

    initAuth() {
        // Update UI based on authentication state
        authService.updateUI();
        
        // Add authentication requirements for protected pages
        if (this.currentPage === 'student-upload' || this.currentPage === 'dashboard') {
            authService.requireAuth();
        }
        
        if (this.currentPage === 'teacher-dashboard') {
            authService.requireRole('teacher');
        }
    }

    initPageHandlers() {
        switch (this.currentPage) {
            case 'login':
                this.initLoginPage();
                break;
            case 'signup':
            case 'teacher-signup':
                this.initSignupPage();
                break;
            case 'student-upload':
                this.initStudentUploadPage();
                break;
            case 'teacher-dashboard':
                this.initTeacherDashboardPage();
                break;
            case 'dashboard':
                this.initDashboardPage();
                break;
            case 'index':
                this.initHomePage();
                break;
        }
    }

    initLoginPage() {
        const loginForm = document.querySelector('form');
        if (loginForm) {
            loginForm.addEventListener('submit', AuthUtils.handleLogin);
        }
    }

    initSignupPage() {
        const signupForm = document.querySelector('form');
        if (signupForm) {
            signupForm.addEventListener('submit', AuthUtils.handleRegister);
            
            // Handle role selection
            const roleInputs = document.querySelectorAll('input[type="radio"]');
            roleInputs.forEach(input => {
                input.addEventListener('change', (e) => {
                    const role = e.target.value || e.target.parentElement.textContent.trim().toLowerCase();
                    console.log('Selected role:', role);
                    // Add name attribute if missing
                    if (!input.hasAttribute('name')) {
                        input.setAttribute('name', 'role');
                    }
                    // Add value attribute if missing
                    if (!input.hasAttribute('value')) {
                        input.setAttribute('value', role);
                    }
                });
            });
            
            // Set default role if not set
            const hasSelectedRole = Array.from(roleInputs).some(input => input.checked);
            if (!hasSelectedRole && roleInputs.length > 0) {
                roleInputs[0].checked = true;
                const event = new Event('change');
                roleInputs[0].dispatchEvent(event);
            }
        }
    }

    initStudentUploadPage() {
        const uploadForm = document.getElementById('upload-form');
        const fileInput = document.getElementById('file-input');
        const titleInput = document.getElementById('title-input');
        const uploadButton = document.getElementById('upload-button');
        const analyzeButton = document.getElementById('analyze-button');
        
        if (uploadForm && fileInput && titleInput) {
            // File selection handler
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    if (!APIUtils.validateFileType(file)) {
                        APIUtils.showError('Invalid file type. Please upload PDF, DOCX, or TXT files.');
                        fileInput.value = '';
                        return;
                    }
                    
                    const fileSize = APIUtils.formatFileSize(file.size);
                    console.log(`Selected file: ${file.name} (${fileSize})`);
                }
            });
            
            // File selection handler - trigger file input when button is clicked
            uploadButton.addEventListener('click', () => {
                fileInput.click();
            });
            
            // File selection handler
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    if (!APIUtils.validateFileType(file)) {
                        APIUtils.showError('Invalid file type. Please upload PDF, DOCX, or TXT files.');
                        fileInput.value = '';
                        return;
                    }
                    
                    const fileSize = APIUtils.formatFileSize(file.size);
                    console.log(`Selected file: ${file.name} (${fileSize})`);
                    
                    // Update button text to show selected file
                    uploadButton.textContent = `Selected: ${file.name}`;
                    
                    // Check if we have both file and title to enable upload
                    if (titleInput.value.trim()) {
                        this.enableUpload();
                    }
                }
            });
            
            // Title input handler
            titleInput.addEventListener('input', () => {
                if (fileInput.files[0] && titleInput.value.trim()) {
                    this.enableUpload();
                }
            });
            
            // Analyze handler
            if (analyzeButton) {
                analyzeButton.addEventListener('click', async () => {
                    if (!window.uploadedFileId) {
                        APIUtils.showError('Please upload a file first.');
                        return;
                    }
                    
                    try {
                        analyzeButton.disabled = true;
                        analyzeButton.textContent = 'Analyzing...';
                        
                        console.log(`Starting analysis for file ID: ${window.uploadedFileId}`);
                        
                        const result = await apiService.analyzeFile(window.uploadedFileId, authService.getAuthToken());
                        console.log('Analysis result:', result);
                        
                        if (!result || !result.plagiarism_score) {
                            throw new Error('Invalid analysis result from server');
                        }
                        
                        // Show results
                        this.showAnalysisResults(result);
                        
                    } catch (error) {
                        console.error('Analysis error:', error);
                        APIUtils.showError('Analysis failed: ' + error.message);
                    } finally {
                        analyzeButton.disabled = false;
                        analyzeButton.textContent = 'Analyze Document';
                    }
                });
            }
        }
    }
    
    enableUpload() {
        const uploadForm = document.getElementById('upload-form');
        const fileInput = document.getElementById('file-input');
        const titleInput = document.getElementById('title-input');
        const analyzeButton = document.getElementById('analyze-button');
        
        // Remove existing upload button if it exists
        const existingUploadBtn = document.getElementById('actual-upload-button');
        if (existingUploadBtn) {
            existingUploadBtn.remove();
        }
        
        // Create new upload button
        const uploadButton = document.createElement('button');
        uploadButton.id = 'actual-upload-button';
        uploadButton.className = 'flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-4 bg-[#1383eb] text-white text-sm font-bold leading-normal tracking-[0.015em] mt-4';
        uploadButton.textContent = 'Upload File';
        
        uploadForm.appendChild(uploadButton);
        
        // Upload handler
        uploadButton.addEventListener('click', async () => {
            const file = fileInput.files[0];
            const title = titleInput.value.trim();
            
            if (!file || !title) {
                APIUtils.showError('Please select a file and enter a title.');
                return;
            }
            
            try {
                uploadButton.disabled = true;
                uploadButton.textContent = 'Uploading...';
                
                const result = await apiService.uploadFile(file, title, authService.getAuthToken());
                
                APIUtils.showSuccess('File uploaded successfully!');
                
                // Store file ID for analysis
                window.uploadedFileId = result.file_id;
                
                // Enable analyze button
                if (analyzeButton) {
                    analyzeButton.disabled = false;
                    analyzeButton.textContent = 'Analyze Document';
                }
                
                // Hide upload button after successful upload
                uploadButton.style.display = 'none';
                
                            } catch (error) {
                    console.error('Upload error:', error);
                    APIUtils.showError('Upload failed: ' + error.message);
                    
                    // Show more detailed error information
                    if (error.message.includes('Network error')) {
                        console.error('Network error detected. Please check if the backend server is running on http://localhost:8000');
                    }
                } finally {
                    uploadButton.disabled = false;
                    uploadButton.textContent = 'Upload File';
                }
        });
    }

    showAnalysisResults(results) {
        const resultsDiv = document.createElement('div');
        resultsDiv.className = 'mt-6 p-4 bg-[#192733] rounded-lg border border-[#233648]';
        resultsDiv.innerHTML = `
            <h3 class="text-white text-lg font-bold mb-4">Analysis Results</h3>
            <div class="space-y-3">
                <div>
                    <span class="text-[#92aec9]">Plagiarism Score: </span>
                    <span class="text-white font-bold">${(results.plagiarism_score * 100).toFixed(1)}%</span>
                </div>
                <div>
                    <span class="text-[#92aec9]">Summary: </span>
                    <p class="text-white text-sm mt-1">${results.summary}</p>
                </div>
                <div>
                    <span class="text-[#92aec9]">IPFS CID: </span>
                    <span class="text-white font-mono text-sm">${results.ipfs_cid}</span>
                </div>
            </div>
            <div class="mt-4">
                <button id="mint-nft-btn" class="bg-[#1383eb] text-white px-4 py-2 rounded-lg text-sm font-bold">
                    Mint as NFT
                </button>
            </div>
        `;
        
        // Insert results after the form
        const form = document.getElementById('upload-form');
        if (form) {
            form.parentNode.insertBefore(resultsDiv, form.nextSibling);
        }
        
        // Handle mint NFT button
        const mintButton = document.getElementById('mint-nft-btn');
        if (mintButton) {
            mintButton.addEventListener('click', async () => {
                try {
                    mintButton.disabled = true;
                    mintButton.textContent = 'Preparing Metadata...';
                    
                    console.log('Preparing NFT metadata...');
                    const mintData = {
                        title: document.getElementById('title-input').value,
                        summary: results.summary,
                        plagiarism_score: results.plagiarism_score,
                        wallet_address: 'mock_wallet_address', // In real app, get from wallet
                        ipfs_cid: results.ipfs_cid,
                        timestamp: new Date().toISOString()
                    };
                    console.log('Metadata prepared:', mintData);
                    
                    mintButton.textContent = 'Minting NFT...';
                    console.log('Sending mint request to API...');
                    const mintResult = await apiService.mintNFT(mintData, authService.getAuthToken());
                    console.log('Mint result:', mintResult);
                    
                    if (!mintResult || !mintResult.transaction_hash) {
                        throw new Error('Invalid response from server');
                    }
                    
                    APIUtils.showSuccess('NFT minted successfully! Transaction: ' + mintResult.transaction_hash);
                    
                    // Redirect to dashboard
                    mintButton.textContent = 'Redirecting to Dashboard...';
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 2000);
                    
                } catch (error) {
                    console.error('Minting error:', error);
                    APIUtils.showError('Minting failed: ' + error.message);
                } finally {
                    mintButton.disabled = false;
                    mintButton.textContent = 'Mint as NFT';
                }
            });
        }
    }

    initTeacherDashboardPage() {
        this.loadTeacherSubmissions();
    }

    async loadTeacherSubmissions() {
        try {
            const nfts = await apiService.getNFTs(authService.getAuthToken());
            this.displayTeacherSubmissions(nfts);
        } catch (error) {
            console.error('Failed to load submissions:', error);
            APIUtils.showError('Failed to load submissions');
        }
    }

    displayTeacherSubmissions(nfts) {
        const tableBody = document.querySelector('tbody');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        nfts.forEach(nft => {
            const row = document.createElement('tr');
            row.className = 'border-t border-t-[#324f67]';
            row.innerHTML = `
                <td class="h-[72px] px-4 py-2 w-[400px] text-white text-sm font-normal leading-normal">
                    ${nft.student_name || 'Unknown Student'}
                </td>
                <td class="h-[72px] px-4 py-2 w-[400px] text-[#92b0c9] text-sm font-normal leading-normal">
                    ${nft.title}
                </td>
                <td class="h-[72px] px-4 py-2 w-[400px] text-[#92b0c9] text-sm font-normal leading-normal">
                    ${new Date(nft.timestamp).toLocaleDateString()}
                </td>
                <td class="h-[72px] px-4 py-2 w-60 text-[#92b0c9] text-sm font-bold leading-normal tracking-[0.015em]">
                    <button onclick="app.viewSubmission('${nft.id}')" class="text-[#1383eb] hover:underline">View</button> | 
                    <button onclick="app.verifySubmission('${nft.id}')" class="text-[#1383eb] hover:underline">Verify</button> | 
                    <button onclick="app.giveFeedback('${nft.id}')" class="text-[#1383eb] hover:underline">Feedback</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    viewSubmission(nftId) {
        // Implement view submission functionality
        console.log('Viewing submission:', nftId);
        APIUtils.showSuccess('Viewing submission...');
    }

    verifySubmission(nftId) {
        // Implement verification functionality
        console.log('Verifying submission:', nftId);
        APIUtils.showSuccess('Submission verified!');
    }

    giveFeedback(nftId) {
        // Implement feedback functionality
        console.log('Giving feedback for:', nftId);
        const feedback = prompt('Enter your feedback:');
        if (feedback) {
            // Submit feedback to backend
            apiService.submitTeacherComment({
                nft_id: nftId,
                feedback: feedback
            }, authService.getAuthToken()).then(() => {
                APIUtils.showSuccess('Feedback submitted successfully!');
            }).catch(error => {
                APIUtils.showError('Failed to submit feedback: ' + error.message);
            });
        }
    }

    initDashboardPage() {
        this.loadUserNFTs();
    }

    async loadUserNFTs() {
        try {
            console.log('Loading user NFTs...');
            const nfts = await apiService.getNFTs(authService.getAuthToken());
            console.log('NFTs loaded:', nfts);
            this.displayUserNFTs(nfts);
            
            // Update stats
            this.updateDashboardStats(nfts);
        } catch (error) {
            console.error('Failed to load NFTs:', error);
            const container = document.getElementById('nfts-container');
            if (container) {
                container.innerHTML = `
                    <div class="text-center py-8">
                        <p class="text-red-400 text-lg">Failed to load NFTs</p>
                        <p class="text-[#92aec9] text-sm mt-2">${error.message}</p>
                        <button onclick="app.loadUserNFTs()" class="inline-block mt-4 bg-[#1383eb] text-white px-6 py-2 rounded-lg">
                            Retry
                        </button>
                    </div>
                `;
            }
        }
    }
    
    updateDashboardStats(nfts) {
        const totalDocs = document.getElementById('total-docs');
        const totalNfts = document.getElementById('total-nfts');
        const avgScore = document.getElementById('avg-score');
        
        if (totalDocs) totalDocs.textContent = nfts.length;
        if (totalNfts) totalNfts.textContent = nfts.length;
        
        if (avgScore && nfts.length > 0) {
            const avgPlagiarism = nfts.reduce((sum, nft) => sum + (nft.plagiarism_score || 0), 0) / nfts.length;
            avgScore.textContent = `${((1 - avgPlagiarism) * 100).toFixed(1)}%`;
        }
    }

    displayUserNFTs(nfts) {
        const container = document.getElementById('nfts-container');
        if (!container) return;
        
        if (nfts.length === 0) {
            container.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-[#92aec9] text-lg">No NFTs found</p>
                    <p class="text-[#92aec9] text-sm mt-2">Upload your first document to create an NFT</p>
                    <a href="student_upload.html" class="inline-block mt-4 bg-[#1383eb] text-white px-6 py-2 rounded-lg">
                        Upload Document
                    </a>
                </div>
            `;
            return;
        }
        
        container.innerHTML = nfts.map(nft => `
            <div class="bg-[#192733] rounded-lg p-4 border border-[#233648]">
                <h3 class="text-white font-bold text-lg">${nft.title}</h3>
                <p class="text-[#92aec9] text-sm mt-2">${nft.summary}</p>
                <div class="flex justify-between items-center mt-4">
                    <span class="text-[#92aec9] text-sm">Plagiarism: ${(nft.plagiarism_score * 100).toFixed(1)}%</span>
                    <span class="text-[#92aec9] text-sm">${new Date(nft.timestamp).toLocaleDateString()}</span>
                </div>
                ${nft.teacher_feedback ? `
                    <div class="mt-3 p-3 bg-[#233648] rounded">
                        <p class="text-[#92aec9] text-sm font-bold">Teacher Feedback:</p>
                        <p class="text-white text-sm">${nft.teacher_feedback}</p>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    initHomePage() {
        // Add any home page specific functionality
        console.log('Home page initialized');
    }

    async checkAPIHealth() {
        try {
            const isHealthy = await apiService.checkHealth();
            if (!isHealthy) {
                console.warn('API is not responding');
                // You could show a warning to users here
            }
        } catch (error) {
            console.error('API health check failed:', error);
        }
    }

    setupGlobalListeners() {
        // Handle navigation
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href^="#"]')) {
                e.preventDefault();
                const href = e.target.getAttribute('href');
                if (href === '#logout') {
                    authService.logout();
                }
            }
        });
        
        // Handle form submissions globally
        document.addEventListener('submit', (e) => {
            if (e.target.matches('form')) {
                const action = e.target.getAttribute('data-action');
                console.log('Form submitted with action:', action);
                
                if (action === 'login') {
                    e.preventDefault();
                    AuthUtils.handleLogin(e);
                } else if (action === 'register') {
                    e.preventDefault();
                    AuthUtils.handleRegister(e);
                }
            }
        });
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AcademicNFTApp();
});

// Export for global access
window.AcademicNFTApp = AcademicNFTApp; 