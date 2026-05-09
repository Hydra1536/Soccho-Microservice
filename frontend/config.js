// API Configuration for Soccho Microservices
// Maps frontend API endpoints to their corresponding Render services

const API_CONFIG = {
  // Service endpoints
  SERVICES: {
    // IMPORTANT: the frontend should call the gateway for auth routes.
    // The auth service itself exposes routes under /api/..., while the gateway exposes /auth/...
    GATEWAY: 'https://soccho-gateway.onrender.com',
    AUTH: 'https://soccho-auth.onrender.com',
    SOCIAL: 'https://soccho-social.onrender.com',
    TRANSACTIONS: 'https://soccho-transaction.onrender.com',
    NOTIFICATIONS_WS: 'wss://soccho-notification.onrender.com',
  },

  // Local development endpoints
  LOCAL_SERVICES: {
    GATEWAY: 'http://localhost:8000',
    AUTH: 'http://localhost:8001',
    SOCIAL: 'http://localhost:8002',
    TRANSACTIONS: 'http://localhost:8003',
    NOTIFICATIONS_WS: 'ws://localhost:8004',
  },

  // Route mapping: endpoint pattern -> service
  ROUTE_MAP: {
    '/auth': 'GATEWAY',
    '/social': 'GATEWAY',
    '/transactions': 'GATEWAY',
    '/notifications': 'NOTIFICATIONS_WS',
  },

  isDevelopment: function() {
    return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  },

  getServices: function() {
    return this.isDevelopment() ? this.LOCAL_SERVICES : this.SERVICES;
  },

  getServiceUrl: function(endpoint) {
    const services = this.getServices();
    
    // Check if it's a WebSocket endpoint
    if (endpoint.includes('/ws/') || endpoint === '/ws') {
      return services.NOTIFICATIONS_WS;
    }

    // Find matching route
    for (let pattern in this.ROUTE_MAP) {
      if (endpoint.startsWith(pattern)) {
        const serviceName = this.ROUTE_MAP[pattern];
        return services[serviceName];
      }
    }

    // Default to gateway
    return services.GATEWAY;
  },

  buildFullUrl: function(endpoint) {
    if (endpoint.startsWith('http://') || endpoint.startsWith('https://') || 
        endpoint.startsWith('ws://') || endpoint.startsWith('wss://')) {
      return endpoint;
    }
    const baseUrl = this.getServiceUrl(endpoint);
    return baseUrl + endpoint;
  },

  init: function() {
    const services = this.getServices();
    window.API_GATEWAY = services.GATEWAY;
    window.API_CONFIG = this;

    // Intercept HTMX requests to use proper service URLs
    if (window.htmx) {
      document.addEventListener('htmx:ajax:beforeRequest', (evt) => {
        const path = evt.detail.path;
        if (path && path.startsWith('/') && !path.includes('://')) {
          evt.detail.path = this.buildFullUrl(path);
        }
      });
    }

    console.log('[Soccho API Config] Initialized', {
      environment: this.isDevelopment() ? 'development' : 'production',
      gateway: services.GATEWAY,
    });
  }
};

// Initialize on script load
API_CONFIG.init();

// Utility function for fetch API calls
async function apiCall(method, endpoint, data = null, options = {}) {
  const url = API_CONFIG.buildFullUrl(endpoint);
  const fetchOptions = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include',
    ...options,
  };

  if (data) {
    fetchOptions.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, fetchOptions);
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText} (${response.status})`);
    }
    return response;
  } catch (error) {
    console.error('[API Error]', endpoint, error);
    throw error;
  }
}

// Utility function to get WebSocket URL
function getWebSocketUrl(endpoint) {
  const url = API_CONFIG.buildFullUrl(endpoint);
  return url;
}
