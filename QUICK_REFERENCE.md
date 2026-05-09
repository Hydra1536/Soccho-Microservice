# Soccho Frontend - Quick Reference

## Service URLs

### Production (Render)
```
Gateway:      https://soccho-gateway.onrender.com
Auth:         https://soccho-auth.onrender.com
Social:       https://soccho-social.onrender.com
Transactions: https://soccho-transaction.onrender.com
Notifications: wss://soccho-notification.onrender.com
```

### Local Development
```
Gateway:      http://localhost:8000
Auth:         http://localhost:8001
Social:       http://localhost:8002
Transactions: http://localhost:8003
Notifications: ws://localhost:8004
```

---

## API Endpoints (via Gateway)

### Authentication
```
POST   /auth/login          - Login user
POST   /auth/register       - Register new user
POST   /auth/forgot-password - Request password reset
POST   /auth/otp-verify     - Verify OTP
GET    /auth/google/login   - Google OAuth
GET    /auth/user           - Get current user
POST   /auth/logout         - Logout user
```

### Social/Friends
```
GET    /social/friends      - List user's friends
GET    /social/search       - Search for friends
POST   /social/add-friend   - Send friend request
POST   /social/accept       - Accept friend request
POST   /social/remove       - Remove friend
```

### Transactions
```
POST   /transactions/create - Create new transaction
GET    /transactions/list   - List transactions
GET    /transactions/{id}   - Get transaction details
PUT    /transactions/{id}   - Update transaction
DELETE /transactions/{id}   - Delete transaction
POST   /transactions/pay    - Mark as paid
```

### Notifications (WebSocket)
```
ws://localhost:8004/ws/notifications/
wss://soccho-notification.onrender.com/ws/notifications/
```

---

## Code Examples

### HTMX Form (Automatic Routing)
```html
<form hx-post="/auth/login" hx-target="#result">
  <input type="email" name="email" required />
  <input type="password" name="password" required />
  <button type="submit">Login</button>
</form>
```

### Fetch API Call
```javascript
// Login
const response = await apiCall('POST', '/auth/login', {
  email: 'user@example.com',
  password: 'password123'
});
const data = await response.json();

// Get friends
const friends = await apiCall('GET', '/social/friends');
const friendsList = await friends.json();

// Create transaction
const txn = await apiCall('POST', '/transactions/create', {
  friend_id: 123,
  amount: 50.00,
  description: 'Lunch'
});
```

### WebSocket Connection
```javascript
const ws = new WebSocket(getWebSocketUrl('/ws/notifications/'));

ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => {
  const notification = JSON.parse(e.data);
  console.log('Notification:', notification);
};
ws.onerror = (e) => console.error('Error:', e);
ws.onclose = () => console.log('Closed');

// Send to server
ws.send(JSON.stringify({ action: 'mark_read', id: 123 }));
```

### Using NotificationManager
```javascript
// In HTML:
// <script src="config.js"></script>
// <script src="/static/js/notification-manager.js"></script>

const notifyManager = new NotificationManager();

notifyManager.on('notification', (notif) => {
  console.log('New notification:', notif);
});

notifyManager.on('connected', () => {
  console.log('Connected to notification service');
});

// Mark notification as read
notifyManager.markAsRead(notificationId);

// Check if connected
if (notifyManager.isConnected()) {
  console.log('Ready to receive notifications');
}

// Close connection
notifyManager.close();

// Reconnect
notifyManager.reconnect();
```

---

## Debugging

### Check Configuration
```javascript
console.log(API_CONFIG);
console.log(API_CONFIG.getServices());
```

### Build Full URL
```javascript
API_CONFIG.buildFullUrl('/auth/login');
// Production: https://soccho-gateway.onrender.com/auth/login
// Local: http://localhost:8000/auth/login
```

### Test API Endpoint
```javascript
apiCall('GET', '/auth/user')
  .then(r => r.json())
  .then(d => console.log('User:', d))
  .catch(e => console.error('Error:', e));
```

### Monitor HTMX Requests
```javascript
// Enable debug logging
htmx.config.debugLoggingEnabled = true;

// Listen for events
document.body.addEventListener('htmx:afterRequest', (e) => {
  console.log('Status:', e.detail.xhr.status);
  console.log('Endpoint:', e.detail.path);
});
```

### Check Environment
```javascript
API_CONFIG.isDevelopment();  // true/false
API_CONFIG.SERVICES;          // Production URLs
API_CONFIG.LOCAL_SERVICES;    // Local URLs
```

---

## File Locations

| File | Purpose |
|------|---------|
| `frontend/config.js` | API configuration & routing |
| `frontend/index.html` | Login/Register page |
| `frontend/manifest.json` | PWA manifest |
| `frontend/icon.svg` | PWA icon |
| `frontend/vercel.json` | Vercel deployment config |
| `frontend/static/js/app.js` | Main app logic |
| `frontend/static/js/notification-manager.js` | WebSocket handler |
| `frontend/static/js/app-enhanced.js` | Enhanced app example |
| `notification_service/notification_service/asgi.py` | Django ASGI app |
| `notification_service/notifications/models.py` | Notification model |

---

## Browser Console Commands

```javascript
// Check if config is loaded
console.log(typeof API_CONFIG);  // 'object'

// Get all services
const services = API_CONFIG.getServices();
console.log(services);

// Build URLs
console.log(API_CONFIG.buildFullUrl('/auth/login'));
console.log(API_CONFIG.buildFullUrl('/ws/notifications/'));

// Test endpoint
apiCall('GET', '/auth/user').then(r => r.json()).then(console.log);

// Enable HTMX debug
htmx.config.debugLoggingEnabled = true;

// Check HTMX version
console.log(htmx.version);

// Check if notification manager loaded
console.log(typeof NotificationManager);

// List all HTMX listeners
Object.keys(htmx.on);
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 404 errors | Check URL in Network tab matches service endpoint |
| CORS errors | Verify service has correct CORS headers |
| WebSocket fails | Ensure using `wss://` for production |
| HTMX not routing | Verify `config.js` loads before HTMX |
| Notifications not working | Check notification service is running |
| Offline errors | Service Worker caches some routes |

---

## Performance Tips

- ✅ Use HTMX for simple forms (auto-routed)
- ✅ Use `apiCall()` for complex requests
- ✅ Cache user data in IndexedDB for offline
- ✅ Use WebSockets only for real-time data
- ✅ Implement request debouncing for search
- ✅ Add loading states to UX

---

## Security Reminders

- ✅ CORS configured for frontend domain only
- ✅ JWT tokens sent in credentials (cookies)
- ✅ All endpoints support authentication
- ✅ Rate limiting enabled on gateway
- ✅ Security headers configured
- ⚠️ Never expose secrets in frontend code
- ⚠️ Always use HTTPS in production
- ⚠️ Validate all user input on backend

---

**Last Updated**: May 9, 2026
**Status**: Production Ready
