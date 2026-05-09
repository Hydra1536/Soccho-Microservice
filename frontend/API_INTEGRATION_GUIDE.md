# Soccho Frontend - API Integration Guide

## Overview

All frontend API endpoints are now properly configured to route to your Render microservices. The configuration is automatically handled by `config.js` which loads before HTMX.

## Service Mapping

### Production (Render)
- **Gateway API**: https://soccho-gateway.onrender.com (main entry point)
- **Auth Service**: https://soccho-auth.onrender.com
- **Social Service**: https://soccho-social.onrender.com
- **Transactions Service**: https://soccho-transaction.onrender.com
- **Notifications Service**: wss://soccho-notification.onrender.com (WebSocket)

### Local Development
- **Gateway**: http://localhost:8000
- **Auth**: http://localhost:8001
- **Social**: http://localhost:8002
- **Transactions**: http://localhost:8003
- **Notifications**: ws://localhost:8004 (WebSocket)

## How It Works

### 1. HTMX Integration (Automatic)

All HTMX requests with relative paths are automatically intercepted and routed to the correct service:

```html
<!-- These relative paths are automatically converted to absolute URLs -->
<form hx-post="/auth/login" hx-target="#result">
  <!-- Automatically becomes: https://soccho-gateway.onrender.com/auth/login -->
</form>

<div hx-get="/social/friends" hx-trigger="load">
  <!-- Automatically becomes: https://soccho-gateway.onrender.com/social/friends -->
</div>
```

**Status**: ✅ Already implemented in all HTML files

### 2. Fetch API Calls (Manual)

Use the provided `apiCall()` utility function for fetch requests:

```javascript
// Example: Login request
async function login(email, password) {
  try {
    const response = await apiCall('POST', '/auth/login', {
      email,
      password
    });
    const data = await response.json();
    console.log('Login successful:', data);
  } catch (error) {
    console.error('Login failed:', error);
  }
}

// Example: Get user friends
async function getFriends() {
  try {
    const response = await apiCall('GET', '/social/friends');
    const friends = await response.json();
    return friends;
  } catch (error) {
    console.error('Failed to fetch friends:', error);
  }
}

// Example: Create transaction
async function createTransaction(friendId, amount) {
  try {
    const response = await apiCall('POST', '/transactions/create', {
      friend_id: friendId,
      amount: amount
    });
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Transaction failed:', error);
  }
}
```

### 3. WebSocket Connections

For real-time notifications, use the `getWebSocketUrl()` function:

```javascript
// Example: Connect to notification WebSocket
function connectNotifications() {
  const wsUrl = getWebSocketUrl('/ws/notifications/');
  const ws = new WebSocket(wsUrl);

  ws.addEventListener('open', () => {
    console.log('Connected to notifications');
  });

  ws.addEventListener('message', (event) => {
    const notification = JSON.parse(event.data);
    console.log('New notification:', notification);
    // Handle notification display
  });

  ws.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
  });

  ws.addEventListener('close', () => {
    console.log('Disconnected from notifications');
    // Implement reconnection logic
  });

  return ws;
}
```

## Implementation Examples

### Example 1: Form Submission with HTMX

```html
<!-- No changes needed! This automatically uses the correct API endpoint -->
<form hx-post="/auth/register" hx-target="#result" hx-swap="innerHTML">
  <input type="email" name="email" required />
  <input type="password" name="password" required />
  <button type="submit">Register</button>
</form>

<!-- Result container -->
<div id="result"></div>
```

### Example 2: Dynamic Data Loading

```html
<!-- Loading friends list - automatically routes to social service -->
<div id="friends" hx-get="/social/friends" hx-trigger="load" hx-swap="innerHTML">
  Loading friends...
</div>
```

### Example 3: Custom JavaScript with Fetch

```javascript
// app.js
class NotificationManager {
  constructor() {
    this.ws = null;
    this.connect();
  }

  connect() {
    const wsUrl = getWebSocketUrl('/ws/notifications/');
    this.ws = new WebSocket(wsUrl);
    
    this.ws.onopen = () => this.handleConnected();
    this.ws.onmessage = (e) => this.handleMessage(e);
    this.ws.onerror = (e) => this.handleError(e);
    this.ws.onclose = () => this.handleDisconnected();
  }

  handleConnected() {
    console.log('Notification WebSocket connected');
    document.body.classList.remove('disconnected');
  }

  handleMessage(event) {
    const data = JSON.parse(event.data);
    this.displayNotification(data);
  }

  handleError(error) {
    console.error('WebSocket error:', error);
  }

  handleDisconnected() {
    console.log('Notification WebSocket disconnected');
    document.body.classList.add('disconnected');
    // Reconnect after 3 seconds
    setTimeout(() => this.connect(), 3000);
  }

  displayNotification(notification) {
    // Show notification in UI
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  new NotificationManager();
});
```

## Debugging

### Check Configuration

Open the browser console and run:

```javascript
console.log(API_CONFIG);
// Shows all available services and routes
```

### Test API Endpoint

```javascript
// Test auth endpoint
apiCall('GET', '/auth/user')
  .then(r => r.json())
  .then(d => console.log('User:', d))
  .catch(e => console.error('Error:', e));
```

### Monitor HTMX Requests

Enable HTMX debug in the console:

```javascript
htmx.config.debugLoggingEnabled = true;
```

## CORS Configuration

The gateway service has CORS configured for:
- Frontend: https://soccho.vercel.app
- Local dev: http://localhost:3000

If you get CORS errors:
1. Check that your service URL is correct
2. Verify CORS headers in the service configuration
3. Ensure credentials are being sent: `credentials: 'include'`

## Status Summary

- ✅ **config.js**: Fully configured with all service endpoints
- ✅ **HTMX Interception**: All relative paths auto-converted to absolute URLs
- ✅ **HTML Files**: All updated with correct script loading order
- ✅ **vercel.json**: Headers configured correctly with regex
- ✅ **manifest.json**: Icon fixed with SVG file reference
- ✅ **ASGI Setup**: notification_service properly initialized

## Next Steps

1. **Test locally**: Set `API_CONFIG.isDevelopment()` to true to test with local services
2. **Monitor**: Use browser DevTools to verify API requests are going to correct URLs
3. **Error Handling**: Implement proper error handlers for network failures
4. **Offline Support**: app.js already has offline detection - enhance with retry logic
