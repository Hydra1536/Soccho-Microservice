# Quick Troubleshooting Guide - Soccho Frontend

## 🔴 Common Issues & Instant Fixes

### **Issue: "Service Unavailable (503)" Error**
```
✅ What's happening: Backend service temporarily down or recovering
✅ What we did: Added automatic retry (3 attempts, max 10 sec)
✅ What you see: "Service temporarily unavailable... retrying" toast
✅ What to do: Wait a few seconds, page will retry automatically
❓ If persists: Check DEPLOYMENT_VERIFICATION.md → Service Status Check
```

### **Issue: "No Tailwind CSS" / Styling broken**
```
✅ What's happening: CSS didn't load
✅ What we did: Moved all CSS to local files (no CDN)
✅ Check in browser:
   1. Open DevTools (F12)
   2. Go to Network tab
   3. Look for: static/css/auth.css
   4. Should be 200 OK
❓ If missing: Verify frontend served from correct directory
```

### **Issue: Form won't submit / "Invalid email"**
```
✅ What's happening: Client-side validation caught an error
✅ What we did: Added email/password validation
✅ Requirements:
   - Email: valid format (e.g., user@example.com)
   - Password: 8+ characters
   - Confirm password: must match
✅ Check: Error message shows exact requirement
✅ Fix: Enter valid data and try again
```

### **Issue: "API call failed" / Mixed protocol errors**
```
✅ What's happening: Frontend trying to call HTTP from HTTPS (or vice versa)
✅ What we did: Added automatic URL routing via config.js
✅ Check in console:
   console.log(API_CONFIG.buildFullUrl('/auth/login'))
   // Should show correct protocol + domain
✅ For production (Vercel):
   // Should output: https://soccho-gateway.onrender.com/...
✅ For local dev:
   // Should output: http://localhost:8000/...
```

### **Issue: Login button not working / Form stuck**
```
✅ What's happening: HTMX form not intercepted or error occurred
✅ Check in console (F12):
   1. Go to Console tab
   2. Look for "hx-" errors
   3. Check Network tab for failed requests
✅ Common causes:
   - config.js not loaded (should load FIRST)
   - API endpoint wrong
   - CORS error (check browser Network tab)
✅ Solution: Refresh page and try again
```

### **Issue: See "Tailwind CDN in production" warning**
```
❌ SHOULD NOT HAPPEN - We fixed this!
✅ What we did: Removed CDN, using local CSS files
✅ If you see this warning:
   1. Clear browser cache (Ctrl+Shift+Delete)
   2. Reload page (Ctrl+F5)
   3. Check Network tab for cdn.tailwindcss.com
   4. Should NOT be there
✅ If warning persists: Check a page wasn't missed (see below)
```

### **Issue: Page shows "404 Not Found" for resources**
```
✅ Common causes:
   - CSS file: static/css/auth.css - Check file exists
   - JS file: static/js/error-handler.js - Check file exists
   - Wrong path in HTML (check relative paths)
✅ Check in Network tab for 404s
✅ Verify file exists in project structure
✅ Check HTML has correct path: <script src="..."></script>
```

---

## 🧪 Quick Tests (Copy-Paste to Console)

### **Test API Config**
```javascript
// Paste in browser console on any page
console.log('Is Development:', API_CONFIG.isDevelopment());
console.log('API URL:', API_CONFIG.buildFullUrl('/auth/login'));
console.log('Services:', API_CONFIG.getServices());
```

### **Test Error Handler**
```javascript
// Should log to console and show toast
showErrorToast('Testing error display!');
showSuccessToast('Testing success display!');
```

### **Test HTMX**
```javascript
// Should be available globally
console.log('HTMX version:', htmx.version);
console.log('Alpine version:', Alpine.version);
```

### **Test LocalStorage (Auth)**
```javascript
// Check if token saved after login
console.log('Auth token:', localStorage.getItem('authToken'));
console.log('User data:', JSON.parse(localStorage.getItem('user')));
```

---

## ✅ Verification Checklist

### On Frontend Load
- [ ] No console errors (F12 → Console)
- [ ] No Tailwind CDN warning
- [ ] No 404s for CSS/JS (F12 → Network)
- [ ] CSS styles applied correctly
- [ ] Forms are interactive

### On Form Submission
- [ ] Request appears in Network tab
- [ ] URL is correct (full URL, not relative)
- [ ] Status is 200/201 (not 503/502)
- [ ] If error, shows user-friendly message
- [ ] Toast notification appears

### Environment Check
```javascript
// Run in console to verify environment
{
  isDev: API_CONFIG.isDevelopment(),
  apiUrl: API_CONFIG.buildFullUrl('/auth/login'),
  wsUrl: API_CONFIG.getWebSocketUrl()
}
```

---

## 📱 Mobile Testing

### iPhone/Safari
- [ ] Pinch to zoom works
- [ ] Buttons clickable (44x44px minimum)
- [ ] Text readable
- [ ] Forms work with mobile keyboard

### Android/Chrome
- [ ] Layout not broken
- [ ] No horizontal scroll
- [ ] Buttons clickable
- [ ] Forms accessible

---

## 🔍 Debugging Workflow

### Step 1: Open DevTools
```
Windows: F12 or Ctrl+Shift+I
Mac: Cmd+Option+I
```

### Step 2: Check Console
```
✅ Should be clean (no red errors)
❌ Any red errors? Note the message
❌ Any "net::ERR"? It's a network/CORS issue
```

### Step 3: Check Network Tab
```
Look for API requests:
✅ URL should be full (starts with http/https)
✅ Status should be 2xx or 4xx (not 503/502)
✅ Response should have data (not empty)
```

### Step 4: Check Styles
```
1. Right-click element → Inspect
2. Check Styles panel
3. Verify CSS file is loaded (auth.css, main.css)
4. Check computed styles section
```

### Step 5: Check Storage
```
1. DevTools → Application → LocalStorage
2. Should have: authToken, user (after login)
3. Check values look reasonable
```

---

## 🆘 When All Else Fails

1. **Clear Cache**
   ```
   Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
   Select: All time, Cookies, Cached images/files
   Clear
   ```

2. **Hard Reload**
   ```
   Ctrl+F5 (or Cmd+Shift+R on Mac)
   Waits for page to fully reload
   ```

3. **Check Backend Status**
   ```
   Open: DEPLOYMENT_VERIFICATION.md
   Follow: Service Status Check section
   Verify all services returning 200 OK
   ```

4. **Check Logs**
   ```
   1. Render Dashboard → Check service logs
   2. Database migrations ran?
   3. Environment variables set?
   4. See DEPLOYMENT_VERIFICATION.md for details
   ```

5. **Ask for Help**
   ```
   Provide:
   - Exact error message (screenshot)
   - Steps to reproduce
   - Browser & device info
   - Network tab screenshot
   - Console errors screenshot
   ```

---

## 📊 Performance Checklist

### Page Load Time
- [ ] Should be < 3 seconds on 3G
- [ ] CSS files load first
- [ ] JS files non-blocking
- [ ] Images optimized

### Network Requests
- [ ] No waterfall of dependent requests
- [ ] Requests happen in parallel
- [ ] No 304 redirects to same resource
- [ ] Gzip compression enabled

### Resource Size
- [ ] CSS files: < 50KB each
- [ ] JS files: < 100KB combined
- [ ] Images: Optimized/compressed
- [ ] No unused resources

---

## 📖 Documentation Reference

| Document | Purpose |
|----------|---------|
| COMPREHENSIVE_FIXES_SUMMARY.md | What was fixed and why |
| FRONTEND_TESTING_GUIDE.md | How to test all features |
| DEPLOYMENT_VERIFICATION.md | Backend verification checklist |
| config.js | API routing configuration |
| error-handler.js | Error handling implementation |
| auth.css | CSS for auth pages |

---

## ⚡ Quick Commands

### Test Locally
```bash
cd frontend
python -m http.server 8080
# Visit http://localhost:8080
```

### Deploy to Vercel
```bash
vercel --prod
# Deploys to production
```

### Check Render Services
```bash
curl -i https://soccho-gateway.onrender.com
curl -i https://soccho-auth.onrender.com:8001
curl -i https://soccho-social.onrender.com:8002
```

---

**Pro Tip:** Most 503 errors resolve themselves in 10-30 seconds. The error handler will automatically retry, so just wait and don't click submit again!

