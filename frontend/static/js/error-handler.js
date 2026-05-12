/**
 * Enhanced API Error Handler with Retry Logic
 * Provides robust error handling, retry mechanisms, and detailed error messages
 */

class APIErrorHandler {
  constructor() {
    this.maxRetries = 3;
    this.retryDelay = 1000; // ms
    this.backoffMultiplier = 2;
    this.errorMessages = {
      503: 'Service unavailable. The server is temporarily down. Please try again in a few moments.',
      502: 'Bad gateway. Connection issue with the server. Please try again.',
      500: 'Server error. Something went wrong on our end. Please try again later.',
      404: 'Not found. The requested resource does not exist.',
      401: 'Unauthorized. Please log in again.',
      403: 'Forbidden. You do not have permission to access this resource.',
      429: 'Too many requests. Please wait a moment before trying again.',
      0: 'Network error. Please check your internet connection.',
    };
  }

  /**
   * Get user-friendly error message
   */
  getErrorMessage(status, error = null) {
    return this.errorMessages[status] || (error?.message || 'An error occurred. Please try again.');
  }

  /**
   * Check if error is retryable
   */
  isRetryable(status) {
    return [503, 502, 500, 429, 0].includes(status);
  }

  /**
   * Enhanced fetch with retry logic
   */
  async fetchWithRetry(url, options = {}, attempt = 1) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!response.ok) {
        const error = new Error(this.getErrorMessage(response.status));
        error.status = response.status;
        throw error;
      }

      return response;
    } catch (error) {
      clearTimeout(timeout);

      // Check if error is retryable
      const status = error.status || 0;
      const isRetryable = this.isRetryable(status);

      if (isRetryable && attempt < this.maxRetries) {
        const delay = this.retryDelay * Math.pow(this.backoffMultiplier, attempt - 1);
        console.log(`[API Error Handler] Retrying in ${delay}ms... (attempt ${attempt}/${this.maxRetries})`);

        await new Promise(resolve => setTimeout(resolve, delay));
        return this.fetchWithRetry(url, options, attempt + 1);
      }

      throw {
        status: status,
        message: this.getErrorMessage(status, error),
        isRetryable: isRetryable,
        attempt: attempt,
      };
    }
  }

  /**
   * Format error for UI display
   */
  formatError(error) {
    if (typeof error === 'string') {
      return error;
    }

    if (error.status === 503) {
      return `⚠️ ${error.message} Services are being restarted. Please wait a moment and refresh.`;
    }

    if (error.status === 0) {
      return `📡 ${error.message}`;
    }

    return `❌ ${error.message}`;
  }
}

// Global error handler instance
const errorHandler = new APIErrorHandler();

/**
 * Enhanced apiCall with error handling
 */
async function apiCallWithErrorHandling(method, endpoint, data = null, options = {}) {
  try {
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

    const response = await errorHandler.fetchWithRetry(url, fetchOptions);

    return response;
  } catch (error) {
    const formattedError = errorHandler.formatError(error);
    console.error('[API Error]', endpoint, error);
    throw {
      message: formattedError,
      details: error,
    };
  }
}

/**
 * Setup global HTMX error handlers
 */
function setupHTMXErrorHandlers() {
  document.addEventListener('htmx:responseError', (evt) => {
    const status = evt.detail.xhr.status;
    const errorMsg = errorHandler.getErrorMessage(status);
    showErrorToast(errorHandler.formatError({ status, message: errorMsg }));
    console.error('[HTMX Error]', status, evt.detail);
  });

  document.addEventListener('htmx:sendError', (evt) => {
    showErrorToast(errorHandler.formatError({ status: 0, message: 'Network error' }));
  });

  document.addEventListener('htmx:timeout', (evt) => {
    showErrorToast('Request timeout. Please try again.');
  });
}

/**
 * Show error toast notification
 */
function showErrorToast(message) {
  // Create toast element if it doesn't exist
  let toastContainer = document.getElementById('error-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'error-toast-container';
    toastContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      max-width: 400px;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.style.cssText = `
    background: #FEF2F2;
    border: 2px solid #FECACA;
    color: #B91C1C;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    animation: slideIn 0.3s ease-out;
  `;
  toast.textContent = message;

  toastContainer.appendChild(toast);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

/**
 * Show success toast notification
 */
function showSuccessToast(message) {
  let toastContainer = document.getElementById('success-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'success-toast-container';
    toastContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      max-width: 400px;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.style.cssText = `
    background: #F0FDF4;
    border: 2px solid #BBFBBB;
    color: #15803D;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    animation: slideIn 0.3s ease-out;
  `;
  toast.textContent = message;

  toastContainer.appendChild(toast);

  // Auto-remove after 4 seconds
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Add animations to document
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }

  .htmx-indicator {
    display: none !important;
  }

  .htmx-indicator.htmx-request {
    display: inline-block !important;
  }
`;
document.head.appendChild(style);

// Initialize error handlers on page load
document.addEventListener('DOMContentLoaded', setupHTMXErrorHandlers);
