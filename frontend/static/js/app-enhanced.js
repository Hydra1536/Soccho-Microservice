/**
 * Enhanced SocchoApp with Notification Support
 * Includes offline support, HTMX error handling, and real-time notifications
 */

class SocchoApp {
  constructor() {
    console.log('[SocchoApp] Initializing...');
    
    this.notificationManager = null;
    this.isOnline = navigator.onLine;

    this.initOfflineSupport();
    this.initHTMXHandlers();
    this.initNotifications();
    this.initServiceWorker();
  }

  /**
   * Handle offline/online state changes
   */
  initOfflineSupport() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      document.body.classList.remove('offline');
      console.log('[SocchoApp] ✓ Online');
      this.showToast('You are back online', 'success');
      
      // Reconnect notifications
      if (this.notificationManager) {
        this.notificationManager.reconnect();
      }
      
      // Sync queued data
      this.syncOfflineData();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      document.body.classList.add('offline');
      console.log('[SocchoApp] ✗ Offline');
      this.showToast('You are offline - changes will sync when back online', 'warning');
    });
  }

  /**
   * Set up HTMX error and response handlers
   */
  initHTMXHandlers() {
    document.body.addEventListener('htmx:responseError', (e) => {
      console.error('[HTMX] Response error:', e.detail);
      this.showToast('Network error. Please try again.', 'error');
    });

    document.body.addEventListener('htmx:sendError', (e) => {
      console.error('[HTMX] Send error:', e.detail);
      this.showToast('Failed to send request', 'error');
    });

    document.body.addEventListener('htmx:sseError', (e) => {
      console.error('[HTMX] SSE error:', e.detail);
    });

    // Log successful requests in development
    if (API_CONFIG.isDevelopment()) {
      document.body.addEventListener('htmx:afterRequest', (e) => {
        if (e.detail.successful) {
          console.log('[HTMX] Request successful:', e.detail.xhr.status, e.detail.verb, e.detail.path);
        }
      });
    }
  }

  /**
   * Initialize real-time notification WebSocket
   */
  initNotifications() {
    if (typeof NotificationManager === 'undefined') {
      console.warn('[SocchoApp] NotificationManager not loaded');
      return;
    }

    this.notificationManager = new NotificationManager({
      maxReconnects: 5,
      reconnectDelay: 3000,
    });

    // Listen for notifications
    this.notificationManager.on('notification', (notification) => {
      this.handleNotification(notification);
    });

    this.notificationManager.on('connected', () => {
      console.log('[SocchoApp] Notification service connected');
      this.updateConnectionStatus(true);
    });

    this.notificationManager.on('disconnected', () => {
      console.log('[SocchoApp] Notification service disconnected');
      this.updateConnectionStatus(false);
    });

    this.notificationManager.on('error', (error) => {
      console.error('[SocchoApp] Notification service error:', error);
    });
  }

  /**
   * Handle incoming notification
   */
  handleNotification(notification) {
    console.log('[SocchoApp] New notification:', notification);

    // Update notification badge
    this.updateNotificationBadge();

    // Play sound if enabled
    this.playNotificationSound();

    // Update UI if on specific pages
    if (notification.type === 'payment_received') {
      this.updateTransactionList();
    }
  }

  /**
   * Register and initialize service worker for offline support
   */
  initServiceWorker() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/static/js/sw.js')
        .then(reg => console.log('[SocchoApp] Service Worker registered'))
        .catch(err => console.log('[SocchoApp] Service Worker registration failed:', err));
    }
  }

  /**
   * Sync offline data when back online
   */
  syncOfflineData() {
    console.log('[SocchoApp] Syncing offline data...');
    // TODO: Implement IndexedDB sync logic
    // - Query pending transactions from IndexedDB
    // - Send to server
    // - Clear from cache on success
  }

  /**
   * Update notification badge count
   */
  updateNotificationBadge() {
    const badge = document.querySelector('[data-notifications-badge]');
    if (badge) {
      const count = parseInt(badge.textContent || 0) + 1;
      badge.textContent = count;
      badge.style.display = count > 0 ? 'block' : 'none';
    }
  }

  /**
   * Play notification sound
   */
  playNotificationSound() {
    // Create or use existing audio element
    const audioId = 'notification-sound';
    let audio = document.getElementById(audioId);
    
    if (!audio) {
      audio = document.createElement('audio');
      audio.id = audioId;
      audio.src = '/static/sounds/notification.mp3';
      audio.preload = 'auto';
      document.body.appendChild(audio);
    }

    audio.currentTime = 0;
    audio.play().catch(e => console.log('[SocchoApp] Could not play sound:', e));
  }

  /**
   * Update connection status in UI
   */
  updateConnectionStatus(isConnected) {
    const statusIndicator = document.getElementById('connection-status');
    if (statusIndicator) {
      statusIndicator.classList.toggle('connected', isConnected);
      statusIndicator.classList.toggle('disconnected', !isConnected);
      statusIndicator.title = isConnected ? 'Connected' : 'Disconnected';
    }
  }

  /**
   * Update transactions list (called when payment received)
   */
  updateTransactionList() {
    const listElement = document.getElementById('transactions-list');
    if (listElement) {
      // Trigger HTMX reload
      htmx.ajax('GET', API_CONFIG.buildFullUrl('/transactions/list'), {
        target: '#transactions-list',
        swap: 'innerHTML',
      });
    }
  }

  /**
   * Show toast notification
   */
  showToast(message, type = 'info') {
    console.log(`[Toast ${type.toUpperCase()}]`, message);
    
    // TODO: Implement toast UI
    // - Create toast element
    // - Show message
    // - Auto-dismiss after 3-5 seconds
    // - Support types: info, success, warning, error
  }

  /**
   * Cleanup on page unload
   */
  destroy() {
    if (this.notificationManager) {
      this.notificationManager.close();
    }
  }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.sochoApp = new SocchoApp();
  });
} else {
  window.sochoApp = new SocchoApp();
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (window.sochoApp) {
    window.sochoApp.destroy();
  }
});

// Export for debugging
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SocchoApp;
}
