# Soccho Deployment Diagnostics Guide

## 🔴 503 Service Unavailable Errors

### Root Causes & Solutions

#### 1. **Render Services Not Running**
**Symptoms:**
- `GET https://soccho-auth.onrender.com/auth/google/login 503 (Service Unavailable)`
- `POST https://soccho-gateway.onrender.com/auth/login 503 (Service Unavailable)`

**Quick Fix:**
```bash
# Check Render deployment status
# 1. Go to https://render.com/dashboard
# 2. Click on each service (soccho-gateway, soccho-auth, soccho-social, etc.)
# 3. Check "Deploy" tab for error messages
# 4. Click "Manual Deploy" to restart failed services
```

**Common Issues:**
- ❌ Database connection failures (PostgreSQL not running)
- ❌ Redis connection issues (cache layer)
- ❌ Environment variables not set
- ❌ Migration failures during startup

#### 2. **Django Database Migrations Not Run**
**Fix:**
```bash
# SSH into Render service
cd /app
python manage.py migrate
python manage.py createsuperuser  # If needed
```

#### 3. **Environment Variables Missing**
**Check in Render Dashboard:**
1. Service Settings → Environment
2. Verify these are set:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=*.render.com,soccho.vercel.app
   ```

#### 4. **Port Configuration**
**Verify in Dockerfile:**
```dockerfile
# Port must match Render settings
EXPOSE 8000  # or 8001, 8002, 8003, 8004
CMD ["gunicorn", "service_name.wsgi", "--bind", "0.0.0.0:8000"]
```

---

## 🟡 Frontend Issues

### Tailwind CSS CDN Warning
```
cdn.tailwindcss.com should not be used in production
```

**Status:** ✅ FIXED
- Replaced with static CSS files (`auth.css`, `main.css`)
- No longer using CDN

### HTMX Form Routing
**Verify all forms have `config.js` loaded FIRST:**
```html
<!-- ✅ Correct -->
<head>
  <script src="config.js"></script>
  <script src="https://unpkg.com/htmx.org@2.0.0"></script>
</head>

<!-- ❌ Wrong -->
<head>
  <script src="https://unpkg.com/htmx.org@2.0.0"></script>
  <script src="config.js"></script>
</head>
```

---

## 🧪 Testing Endpoints

### Test from Browser Console
```javascript
// Test API Config
console.log(API_CONFIG.isDevelopment())  // Should be false in production
console.log(API_CONFIG.buildFullUrl('/auth/login'))
// Should output: https://soccho-gateway.onrender.com/auth/login

// Test with retry logic
apiCallWithErrorHandling('POST', '/auth/login', {
  email: 'test@example.com',
  password: 'password123'
})
.then(r => r.json())
.then(data => console.log('Success:', data))
.catch(err => console.error('Error:', err.message))
```

### Test Specific Endpoints
```bash
# Test Gateway
curl -X POST https://soccho-gateway.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Test Auth Service
curl https://soccho-auth.onrender.com/health

# Test Social Service
curl https://soccho-social.onrender.com/health

# Test Transactions Service
curl https://soccho-transaction.onrender.com/health

# Test Notification Service (WebSocket - harder to test)
# Use browser DevTools Network tab
```

---

## 📋 Deployment Checklist

- [ ] All Render services deployed and running
- [ ] Database migrations completed
- [ ] Environment variables set correctly
- [ ] CORS enabled on gateway for Vercel origin
- [ ] Rate limiting configured (if needed)
- [ ] Error logging set up
- [ ] Frontend config.js points to correct endpoints
- [ ] All HTML files load config.js before HTMX
- [ ] Error handler installed on all forms
- [ ] Service worker registered (optional PWA feature)

---

## 🔗 Useful Links

- Render Dashboard: https://render.com/dashboard
- Vercel Frontend: https://soccho.vercel.app
- Production Gateway: https://soccho-gateway.onrender.com

---

## 📞 Support

If services keep crashing:
1. Check Render logs for errors
2. Verify database is running
3. Check available memory/CPU (may need upgrade)
4. Review Django error logs
5. Ensure all dependencies installed in requirements.txt

**For 503 errors specifically:**
- Wait 2-3 minutes for service to recover
- Manually deploy the service if stuck
- Check if database quota exceeded (common cause)
