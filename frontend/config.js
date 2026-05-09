// API Configuration
// This file handles dynamic API base URL configuration for the frontend

const API_CONFIG = {
  // Determine API base URL based on environment
  getBaseURL: function() {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
    // For production, use the gateway URL from environment or default
    return window.__API_BASE_URL__ || 'https://soccho-gateway.onrender.com';
  },
  
  init: function() {
    const baseURL = this.getBaseURL();
    window.API_BASE_URL = baseURL;
    
    // Intercept HTMX requests to prepend the API base URL
    if (window.htmx) {
      document.addEventListener('htmx:ajax:beforeRequest', (evt) => {
        const path = evt.detail.path;
        if (path && path.startsWith('/') && !path.includes('://')) {
          // Check if it's an API endpoint (starts with /auth, /social, /transactions, etc.)
          if (path.match(/^\/(auth|social|transactions|notifications)\//)) {
            evt.detail.path = baseURL + path;
          }
        }
      });
    }
  }
};

// Initialize on script load (before other scripts)
API_CONFIG.init();

// Utility function to make API calls
async function apiCall(method, endpoint, data = null) {
  const url = API_CONFIG.getBaseURL() + endpoint;
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Send cookies for authentication
  };
  
  if (data) {
    options.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(url, options);
    return response;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}
