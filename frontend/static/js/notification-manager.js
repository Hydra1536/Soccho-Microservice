/**
 * NotificationManager - Handles real-time WebSocket connections to notification service
 * Uses API_CONFIG to dynamically determine WebSocket URL based on environment
 */

class NotificationManager {
  constructor(options = {}) {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = options.maxReconnects || 5;
    this.reconnectDelay = options.reconnectDelay || 3000;
    this.messageHandlers = new Map();
    this.isManualClose = false;

    // Default notification types
    this.notificationTypes = {
      'lend_confirm': 'Lending Confirmation',
      'payment_received': 'Payment Received',
      'due_reminder': 'Due Date Reminder',
    };

    this.connect();
  }

  /**
   * Establish WebSocket connection using API_CONFIG
   */
  connect() {
    try {
      const wsUrl = getWebSocketUrl('/ws/notifications/');
      console.log('[NotificationManager] Connecting to:', wsUrl);
      
      this.ws = new WebSocket(wsUrl);
      this.ws.onopen = () => this.handleOpen();
      this.ws.onmessage = (e) => this.handleMessage(e);
      this.ws.onerror = (e) => this.handleError(e);
      this.ws.onclose = () => this.handleClose();
    } catch (error) {
      console.error('[NotificationManager] Connection error:', error);
      this.scheduleReconnect();
    }
  }

  /**
   * Handle successful connection
   */
  handleOpen() {
    console.log('[NotificationManager] ✓ Connected');
    this.reconnectAttempts = 0;
    this.updateConnectionStatus(true);

    // Emit connected event
    this.emit('connected');
  }

  /**
   * Handle incoming messages
   */
  handleMessage(event) {
    try {
      const data = JSON.parse(event.data);
      console.log('[NotificationManager] Message received:', data);

      // Handle different message types
      if (data.type === 'notification') {
        this.handleNotification(data.payload);
      } else if (data.type === 'action') {
        this.handleAction(data.payload);
      }

      // Emit message event
      this.emit('message', data);
    } catch (error) {
      console.error('[NotificationManager] Failed to parse message:', error);
    }
  }

  /**
   * Handle notification payload
   */
  handleNotification(notification) {
    const notificationType = this.notificationTypes[notification.type] || notification.type;
    
    console.log(`[NotificationManager] ${notificationType}:`, notification);

    // Show browser notification if permitted
    if (Notification.permission === 'granted') {
      new Notification('Soccho - ' + notificationType, {
        body: notification.message || 'New notification received',
        icon: '/icon.svg',
        badge: '/icon.svg',
      });
    }

    // Update UI - emit event for listeners
    this.emit('notification', notification);
  }

  /**
   * Handle action messages
   */
  handleAction(action) {
    console.log('[NotificationManager] Action:', action);
    this.emit('action', action);
  }

  /**
   * Handle connection errors
   */
  handleError(error) {
    console.error('[NotificationManager] ✗ Error:', error);
    this.updateConnectionStatus(false);
    this.emit('error', error);
  }

  /**
   * Handle connection close
   */
  handleClose() {
    console.log('[NotificationManager] Connection closed');
    this.updateConnectionStatus(false);
    this.emit('disconnected');

    if (!this.isManualClose) {
      this.scheduleReconnect();
    }
  }

  /**
   * Schedule reconnection attempt
   */
  scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * this.reconnectAttempts;
      console.log(`[NotificationManager] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('[NotificationManager] Max reconnection attempts reached');
      this.emit('reconnect_failed');
    }
  }

  /**
   * Send message to server
   */
  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('[NotificationManager] WebSocket not connected');
    }
  }

  /**
   * Mark notification as read
   */
  markAsRead(notificationId) {
    this.send({
      action: 'mark_read',
      id: notificationId,
    });
  }

  /**
   * Register event listener
   */
  on(event, callback) {
    if (!this.messageHandlers.has(event)) {
      this.messageHandlers.set(event, []);
    }
    this.messageHandlers.get(event).push(callback);
  }

  /**
   * Unregister event listener
   */
  off(event, callback) {
    if (this.messageHandlers.has(event)) {
      const handlers = this.messageHandlers.get(event);
      const index = handlers.indexOf(callback);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  /**
   * Emit event to listeners
   */
  emit(event, data) {
    if (this.messageHandlers.has(event)) {
      this.messageHandlers.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`[NotificationManager] Error in ${event} handler:`, error);
        }
      });
    }
  }

  /**
   * Update UI connection status
   */
  updateConnectionStatus(isConnected) {
    const statusElement = document.getElementById('notification-status');
    if (statusElement) {
      statusElement.classList.toggle('connected', isConnected);
      statusElement.classList.toggle('disconnected', !isConnected);
    }

    // Update body classes for global styling
    document.body.classList.toggle('notifications-connected', isConnected);
    document.body.classList.toggle('notifications-disconnected', !isConnected);
  }

  /**
   * Gracefully close connection
   */
  close() {
    this.isManualClose = true;
    if (this.ws) {
      this.ws.close();
    }
    console.log('[NotificationManager] Connection closed manually');
  }

  /**
   * Reconnect after being closed
   */
  reconnect() {
    this.isManualClose = false;
    this.reconnectAttempts = 0;
    this.connect();
  }

  /**
   * Get connection status
   */
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

// Request notification permissions on init
if ('Notification' in window && Notification.permission === 'default') {
  Notification.requestPermission();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NotificationManager;
}
