// Decentralized Academic Plagiarism Checker - Frontend JavaScript
// Handles wallet connection, document upload, analysis, and NFT minting

// API endpoint
const API_URL = 'http://localhost:8000';

// Global state
const state = {
    walletConnected: false,
    walletAddress: null,
    fileId: null,
    analysisResults: null,
    nftId: null,
    transactionHash: null,
    ipfsCid: null
};

// DOM elements
const connectWalletBtn = document.getElementById('connectWalletBtn');
const walletAlert = document.getElementById('walletAlert');
const uploadForm = document.getElementById('uploadForm');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const mintingSection = document.getElementById('mintingSection');
const successSection = document.getElementById('successSection');
const mintBtn = document.getElementById('mintBtn');
const progressBar = document.getElementById('progressBar');
const plagiarismBar = document.getElementById('plagiarismBar');
const plagiarismScore = document.getElementById('plagiarismScore');
const plagiarismMessage = document.getElementById('plagiarismMessage');
const summary = document.getElementById('summary');
const txLink = document.getElementById('txLink');
const ipfsLink = document.getElementById('ipfsLink');

// Check if we're on the teacher page
const isTeacherPage = window.location.pathname.includes('teacher.html');
const nftList = isTeacherPage ? document.getElementById('nftList') : null;
const loadingNfts = isTeacherPage ? document.getElementById('loadingNfts') : null;
const noNfts = isTeacherPage ? document.getElementById('noNfts') : null;
const nftTableBody = isTeacherPage ? document.getElementById('nftTableBody') : null;
const feedbackForm = isTeacherPage ? document.getElementById('feedbackForm') : null;

// Initialize wallet connection
async function initWallet() {
    try {
        console.log('Mock wallet initialization');
        
        // Add event listener for wallet button
        connectWalletBtn.addEventListener('click', connectWallet);
        
        // Check if wallet was previously connected
        const connected = localStorage.getItem('walletConnected') === 'true';
        if (connected) {
            const savedAddress = localStorage.getItem('walletAddress');
            if (savedAddress) {
                state.walletConnected = true;
                state.walletAddress = savedAddress;
                
                // Update UI
                connectWalletBtn.textContent = `Connected: ${shortenAddress(savedAddress)}`;
                connectWalletBtn.classList.add('wallet-connected');
                
                if (walletAlert) {
                    walletAlert.classList.add('d-none');
                }
                
                // If on teacher page, load NFTs
                if (isTeacherPage) {
                    loadNFTs();
                }
            } else {
                await connectWallet();
            }
        }
    } catch (error) {
        console.error('Error initializing wallet:', error);
    }
}

// Connect wallet
async function connectWallet() {
    try {
        // Mock wallet connection
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Generate a mock wallet address
        const mockAddress = '0x' + Math.random().toString(16).substring(2, 42);
        
        // Update state
        state.walletConnected = true;
        state.walletAddress = mockAddress;
        
        // Save connection state
        localStorage.setItem('walletConnected', 'true');
        localStorage.setItem('walletAddress', mockAddress);
        
        // Update UI
        connectWalletBtn.textContent = `Connected: ${shortenAddress(mockAddress)}`;
        connectWalletBtn.classList.add('wallet-connected');
        
        if (walletAlert) {
            walletAlert.classList.add('d-none');
        }
        
        console.log('Wallet connected (mock):', { address: mockAddress });
        
        // If on teacher page, load NFTs
        if (isTeacherPage) {
            loadNFTs();
        }
        
    } catch (error) {
        console.error('Error connecting wallet:', error);
        alert('Failed to connect wallet. Please try again.');
    }
}

// Disconnect wallet
async function disconnectWallet() {
    try {
        if (window.aptos) {
            await window.aptos.disconnect();
        }
        
        // Update state
        state.walletConnected = false;
        state.walletAddress = null;
        
        // Save connection state
        localStorage.setItem('walletConnected', 'false');
        
        // Update UI
        connectWalletBtn.textContent = 'Connect Wallet';
        connectWalletBtn.classList.remove('wallet-connected');
        
        if (walletAlert) {
            walletAlert.classList.remove('d-none');
        }
        
        console.log('Wallet disconnected');
    } catch (error) {
        console.error('Error disconnecting wallet:', error);
    }
}

// Shorten address for display
function shortenAddress(address) {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

// Upload document
async function uploadDocument(formData) {
    try {
        showLoading('Uploading document...');
        updateProgress(20);
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const data = {
            file_id: 'mock_file_id_' + Date.now(),
            message: 'File uploaded successfully',
            title: formData.get('title'),
            filename: formData.get('file').name
        };
        
        state.fileId = data.file_id;
        
        updateProgress(40);
        console.log('Document uploaded (mock):', data);
        
        return data;
    } catch (error) {
        console.error('Error uploading document:', error);
        hideLoading();
        alert(`Error uploading document: ${error.message}`);
        throw error;
    }
}

// Analyze document
async function analyzeDocument(fileId) {
    try {
        updateProgress(60);
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const data = {
            plagiarism_score: Math.floor(Math.random() * 30),
            summary: "This is a mock summary of the document. It appears to be an academic paper discussing various concepts and methodologies. The document contains several sections including an introduction, methodology, results, and conclusion. The analysis suggests this is original work with some common academic phrases.",
            ipfs_cid: "mock_ipfs_cid_" + fileId
        };
        
        state.analysisResults = data;
        state.ipfsCid = data.ipfs_cid;
        
        updateProgress(80);
        console.log('Analysis results (mock):', data);
        
        return data;
    } catch (error) {
        console.error('Error analyzing document:', error);
        hideLoading();
        alert(`Error analyzing document: ${error.message}`);
        throw error;
    }
}

// Mint NFT
async function mintNFT() {
    try {
        if (!state.walletConnected) {
            alert('Please connect your wallet first');
            return;
        }
        
        showMinting();
        
        const title = document.getElementById('title').value;
        const { plagiarism_score, summary, ipfs_cid } = state.analysisResults;
        
        const mintData = {
            title,
            summary,
            plagiarism_score,
            ipfs_cid,
            wallet_address: state.walletAddress,
            timestamp: Math.floor(Date.now() / 1000)
        };
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        const data = {
            success: true,
            nft_id: 'mock_nft_id_' + Date.now(),
            transaction_hash: '0x' + Math.random().toString(16).substring(2, 42)
        };
        
        state.nftId = data.nft_id;
        state.transactionHash = data.transaction_hash;
        
        console.log('NFT minted (mock):', data);
        
        showSuccess();
        
        // Update UI with transaction details
        txLink.textContent = shortenAddress(data.transaction_hash);
        txLink.href = `https://explorer.aptoslabs.com/txn/${data.transaction_hash}?network=testnet`;
        
        ipfsLink.textContent = shortenAddress(ipfs_cid);
        ipfsLink.href = `https://ipfs.io/ipfs/${ipfs_cid}`;
        
        return data;
    } catch (error) {
        console.error('Error minting NFT:', error);
        hideMinting();
        alert(`Error minting NFT: ${error.message}`);
        throw error;
    }
}

// Load NFTs (for teacher page)
async function loadNFTs() {
    if (!isTeacherPage) return;
    
    try {
        showLoadingNfts();
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Generate mock NFTs
        const mockNfts = [
            {
                id: 'mock_nft_1',
                title: 'Research on Machine Learning Applications',
                plagiarism_score: 0.15,
                wallet_address: '0x' + Math.random().toString(16).substring(2, 42),
                timestamp: Math.floor(Date.now() / 1000) - 86400,
                summary: 'This paper explores various applications of machine learning in healthcare.',
                ipfs_cid: 'Qm' + Math.random().toString(36).substring(2, 30),
                transaction_hash: '0x' + Math.random().toString(16).substring(2, 42)
            },
            {
                id: 'mock_nft_2',
                title: 'Blockchain Technology in Supply Chain',
                plagiarism_score: 0.08,
                wallet_address: '0x' + Math.random().toString(16).substring(2, 42),
                timestamp: Math.floor(Date.now() / 1000) - 172800,
                summary: 'An analysis of how blockchain can improve supply chain transparency and efficiency.',
                ipfs_cid: 'Qm' + Math.random().toString(36).substring(2, 30),
                transaction_hash: '0x' + Math.random().toString(16).substring(2, 42)
            },
            {
                id: 'mock_nft_3',
                title: 'Quantum Computing: Current State',
                plagiarism_score: 0.22,
                wallet_address: '0x' + Math.random().toString(16).substring(2, 42),
                timestamp: Math.floor(Date.now() / 1000) - 259200,
                summary: 'A review of the current state of quantum computing and its potential applications.',
                ipfs_cid: 'Qm' + Math.random().toString(36).substring(2, 30),
                transaction_hash: '0x' + Math.random().toString(16).substring(2, 42),
                feedback: 'Excellent work on explaining quantum concepts clearly.'
            }
        ];
        
        if (mockNfts.length === 0) {
            showNoNfts();
            return;
        }
        
        renderNFTs(mockNfts);
        showNftList();
        
    } catch (error) {
        console.error('Error loading NFTs:', error);
        showNoNfts();
    }
}

// Render NFTs in table
function renderNFTs(nfts) {
    if (!nftTableBody) return;
    
    nftTableBody.innerHTML = '';
    
    nfts.forEach(nft => {
        const row = document.createElement('tr');
        
        const date = new Date(nft.timestamp * 1000).toLocaleString();
        const score = Math.round(nft.plagiarism_score * 100);
        const scoreClass = score < 30 ? 'success' : score < 70 ? 'warning' : 'danger';
        
        row.innerHTML = `
            <td>${nft.title}</td>
            <td><span class="badge bg-${scoreClass}">${score}%</span></td>
            <td>${shortenAddress(nft.wallet_address)}</td>
            <td>${date}</td>
            <td>
                <button class="btn btn-sm btn-primary view-nft" data-nft-id="${nft.id}">
                    <i class="fas fa-eye me-1"></i>View
                </button>
            </td>
        `;
        
        nftTableBody.appendChild(row);
    });
    
    // Add event listeners to view buttons
    document.querySelectorAll('.view-nft').forEach(button => {
        button.addEventListener('click', () => {
            const nftId = button.getAttribute('data-nft-id');
            viewNFTDetails(nftId, nfts);
        });
    });
}

// View NFT details
function viewNFTDetails(nftId, nfts) {
    const nft = nfts.find(n => n.id === nftId);
    if (!nft) return;
    
    // Populate modal with NFT details
    document.getElementById('modalTitle').textContent = nft.title;
    document.getElementById('modalAddress').textContent = nft.wallet_address;
    document.getElementById('modalTimestamp').textContent = new Date(nft.timestamp * 1000).toLocaleString();
    document.getElementById('modalSummary').textContent = nft.summary;
    
    const score = Math.round(nft.plagiarism_score * 100);
    document.getElementById('modalPlagiarismScore').textContent = `${score}%`;
    
    const plagiarismBar = document.getElementById('modalPlagiarismBar');
    plagiarismBar.style.width = `${score}%`;
    plagiarismBar.className = 'progress-bar';
    if (score < 30) {
        plagiarismBar.classList.add('score-low');
    } else if (score < 70) {
        plagiarismBar.classList.add('score-medium');
    } else {
        plagiarismBar.classList.add('score-high');
    }
    
    document.getElementById('modalIpfsLink').textContent = shortenAddress(nft.ipfs_cid);
    document.getElementById('modalIpfsLink').href = `https://ipfs.io/ipfs/${nft.ipfs_cid}`;
    
    document.getElementById('modalTxLink').textContent = shortenAddress(nft.transaction_hash);
    document.getElementById('modalTxLink').href = `https://explorer.aptoslabs.com/txn/${nft.transaction_hash}?network=testnet`;
    
    // Handle feedback
    document.getElementById('feedbackNftId').value = nft.id;
    
    if (nft.feedback) {
        document.getElementById('modalPreviousFeedback').textContent = nft.feedback;
        document.getElementById('previousFeedbackSection').classList.remove('d-none');
    } else {
        document.getElementById('previousFeedbackSection').classList.add('d-none');
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('nftDetailsModal'));
    modal.show();
}

// Submit feedback
async function submitFeedback(nftId, feedback) {
    try {
        if (!state.walletConnected) {
            alert('Please connect your wallet first');
            return;
        }
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const data = {
            success: true,
            message: 'Feedback submitted successfully'
        };
        
        console.log('Feedback submitted (mock):', data);
        
        alert('Feedback submitted successfully!');
        
        // Reload NFTs to update the list
        loadNFTs();
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('nftDetailsModal'));
        modal.hide();
        
        return data;
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert(`Error submitting feedback: ${error.message}`);
        throw error;
    }
}

// UI Helper functions
function showLoading(message) {
    if (loadingSection) {
        const loadingText = loadingSection.querySelector('p');
        if (loadingText && message) {
            loadingText.innerHTML = `<i class="fas fa-cog fa-spin me-2"></i>${message}`;
        }
        loadingSection.classList.remove('d-none');
    }
    if (uploadForm) {
        uploadForm.classList.add('d-none');
    }
}

function hideLoading() {
    if (loadingSection) {
        loadingSection.classList.add('d-none');
    }
    if (uploadForm) {
        uploadForm.classList.remove('d-none');
    }
}

function updateProgress(percent) {
    if (progressBar) {
        progressBar.style.width = `${percent}%`;
        progressBar.setAttribute('aria-valuenow', percent);
    }
}

function showResults(results) {
    if (resultsSection) {
        resultsSection.classList.remove('d-none');
    }
    
    if (loadingSection) {
        loadingSection.classList.add('d-none');
    }
    
    if (mintBtn) {
        mintBtn.classList.remove('d-none');
    }
    
    // Update plagiarism score
    const score = Math.round(results.plagiarism_score * 100);
    if (plagiarismScore) {
        plagiarismScore.textContent = `${score}%`;
    }
    
    if (plagiarismBar) {
        plagiarismBar.style.width = `${score}%`;
        plagiarismBar.className = 'progress-bar';
        
        if (score < 30) {
            plagiarismBar.classList.add('score-low');
            if (plagiarismMessage) {
                plagiarismMessage.innerHTML = '<i class="fas fa-check-circle text-success me-2"></i>Low similarity detected. Your work appears to be original.';
            }
        } else if (score < 70) {
            plagiarismBar.classList.add('score-medium');
            if (plagiarismMessage) {
                plagiarismMessage.innerHTML = '<i class="fas fa-exclamation-circle text-warning me-2"></i>Moderate similarity detected. Some passages may need revision.';
            }
        } else {
            plagiarismBar.classList.add('score-high');
            if (plagiarismMessage) {
                plagiarismMessage.innerHTML = '<i class="fas fa-times-circle text-danger me-2"></i>High similarity detected. Significant revision recommended.';
            }
        }
    }
    
    // Update summary
    if (summary) {
        summary.textContent = results.summary;
    }
}

function showMinting() {
    if (mintingSection) {
        mintingSection.classList.remove('d-none');
    }
    
    if (resultsSection) {
        resultsSection.classList.add('d-none');
    }
}

function hideMinting() {
    if (mintingSection) {
        mintingSection.classList.add('d-none');
    }
    
    if (resultsSection) {
        resultsSection.classList.remove('d-none');
    }
}

function showSuccess() {
    if (successSection) {
        successSection.classList.remove('d-none');
    }
    
    if (mintingSection) {
        mintingSection.classList.add('d-none');
    }
}

function showLoadingNfts() {
    if (loadingNfts) {
        loadingNfts.classList.remove('d-none');
    }
    
    if (nftList) {
        nftList.classList.add('d-none');
    }
    
    if (noNfts) {
        noNfts.classList.add('d-none');
    }
}

function showNftList() {
    if (nftList) {
        nftList.classList.remove('d-none');
    }
    
    if (loadingNfts) {
        loadingNfts.classList.add('d-none');
    }
    
    if (noNfts) {
        noNfts.classList.add('d-none');
    }
}

function showNoNfts() {
    if (noNfts) {
        noNfts.classList.remove('d-none');
    }
    
    if (loadingNfts) {
        loadingNfts.classList.add('d-none');
    }
    
    if (nftList) {
        nftList.classList.add('d-none');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize wallet
    initWallet();
    
    // Handle form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!state.walletConnected) {
                alert('Please connect your wallet first');
                return;
            }
            
            const title = document.getElementById('title').value;
            const fileInput = document.getElementById('fileUpload');
            
            if (!fileInput.files[0]) {
                alert('Please select a file to upload');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('title', title);
            
            try {
                // Upload document
                const uploadData = await uploadDocument(formData);
                
                // Analyze document
                const analysisResults = await analyzeDocument(uploadData.file_id);
                
                // Show results
                showResults(analysisResults);
                
            } catch (error) {
                console.error('Error processing document:', error);
                hideLoading();
            }
        });
    }
    
    // Handle mint button click
    if (mintBtn) {
        mintBtn.addEventListener('click', async () => {
            if (!state.walletConnected) {
                alert('Please connect your wallet first');
                return;
            }
            
            try {
                await mintNFT();
            } catch (error) {
                console.error('Error minting NFT:', error);
            }
        });
    }
    
    // Handle feedback form submission
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!state.walletConnected) {
                alert('Please connect your wallet first');
                return;
            }
            
            const nftId = document.getElementById('feedbackNftId').value;
            const feedback = document.getElementById('feedbackText').value;
            
            if (!feedback) {
                alert('Please enter feedback');
                return;
            }
            
            try {
                await submitFeedback(nftId, feedback);
            } catch (error) {
                console.error('Error submitting feedback:', error);
            }
        });
    }
    
    // If on teacher page, load NFTs
    if (isTeacherPage && state.walletConnected) {
        loadNFTs();
    }
});