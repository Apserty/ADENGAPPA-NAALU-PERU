// API Base URL
const API_BASE = 'http://localhost:8000/api';

// API Service functions
const apiService = {
    // User authentication
    async register(userData) {
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
            credentials: 'include'
        });
        return await response.json();
    },

    async login(loginData) {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData),
            credentials: 'include'
        });
        return await response.json();
    },

    async logout() {
        const response = await fetch(`${API_BASE}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        return await response.json();
    },

    async getCurrentUser() {
        const response = await fetch(`${API_BASE}/user`, {
            credentials: 'include'
        });
        if (response.status === 401) return null;
        return await response.json();
    },

    // Claims
    async submitPropertyClaim(claimData) {
        const response = await fetch(`${API_BASE}/claims/property`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(claimData),
            credentials: 'include'
        });
        return await response.json();
    },

    async submitMotorClaim(claimData) {
        const response = await fetch(`${API_BASE}/claims/motor`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(claimData),
            credentials: 'include'
        });
        return await response.json();
    },

    async getClaims() {
        const response = await fetch(`${API_BASE}/claims`, {
            credentials: 'include'
        });
        return await response.json();
    },

    // Support
    async submitSupportTicket(ticketData) {
        const response = await fetch(`${API_BASE}/support`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ticketData),
            credentials: 'include'
        });
        return await response.json();
    }
};

// Update your existing form handlers to use the API
// Example for login form:
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const loginData = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };
    
    try {
        const result = await apiService.login(loginData);
        if (result.status === 'success') {
            // Update UI for logged in user
            currentUser = result.user;
            updateUIForLoggedInUser();
            hideLoginModal();
        } else {
            alert(result.detail || 'Login failed');
        }
    } catch (error) {
        alert('Login error: ' + error.message);
    }
});
