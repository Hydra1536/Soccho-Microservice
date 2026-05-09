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
    
    // Configure HTMX to use the correct base URL
    if (window.htmx) {
      document.body.addEventListener('htmx:configRequest', (detail) => {
        const path = detail.detail.parameters.get ? detail.detail.parameters.get('path') : null;
        // Intercept relative URLs and convert to absolute
        if (detail.detail.verb && detail.detail.path && detail.detail.path.startsWith('/')) {
          // This will be handled by the server-side rewrite or client-side JavaScript
        }
      });
    }
  }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => API_CONFIG.init());
} else {
  API_CONFIG.init();
}

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
