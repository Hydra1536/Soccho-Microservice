# Deployment Verification Checklist

## 🎯 Pre-Production Verification (Backend on Render)

Before testing the frontend, ensure all backend services are properly deployed:

### ✅ Service Status Check

Visit each service URL to verify they're running:

1. **Gateway (FastAPI)**
   - URL: https://soccho-gateway.onrender.com
   - Expected: 200 OK (should return welcome page or 404 for root)
   - Test: `curl -i https://soccho-gateway.onrender.com/health` (if endpoint exists)

2. **Auth Service (Django)**
   - URL: https://soccho-auth.onrender.com:8001
   - Expected: 200 OK
   - Test: `curl -i https://soccho-auth.onrender.com:8001/` (may be CSRF protected)

3. **Social Service (Django)**
   - URL: https://soccho-social.onrender.com:8002
   - Expected: 200 OK
   - Test: `curl -i https://soccho-social.onrender.com:8002/`

4. **Transaction Service (Django)**
   - URL: https://soccho-transaction.onrender.com:8003
   - Expected: 200 OK
   - Test: `curl -i https://soccho-transaction.onrender.com:8003/`

5. **Notification Service (Django Channels - WebSocket)**
   - URL: wss://soccho-notification.onrender.com:8004
   - Status: WebSocket endpoint (harder to test via curl)
   - Test via browser console when authenticated

---

## 🔧 Render Dashboard Checks

### For Each Service:

1. **Environment Variables**
   - [ ] `SECRET_KEY` is set
   - [ ] `DATABASE_URL` is set (PostgreSQL)
   - [ ] `ALLOWED_HOSTS` includes domain
   - [ ] `DEBUG=False` for production
   - [ ] Service-specific secrets configured

2. **Health & Logs**
   - [ ] Service shows "deployed" status (green)
   - [ ] No recent errors in logs
   - [ ] Last deploy was recent
   - [ ] No "Service Unavailable" messages

3. **Settings**
   - [ ] Port correctly configured (8000-8004)
   - [ ] Build command successful
   - [ ] Start command correct
   - [ ] No hanging build processes

---

## 🗄️ Database Verification

### PostgreSQL Setup (Render Database)

```sql
-- Connect to Render PostgreSQL
-- Check database exists
\l

-- Verify migrations ran
-- In Django shell on each service:
python manage.py showmigrations --list

-- Should show all migrations marked as [X] (applied)
```

### Checklist:

- [ ] PostgreSQL instance running on Render
- [ ] Database credentials in `DATABASE_URL`
- [ ] All migrations applied (no pending migrations)
- [ ] Test database tables exist
- [ ] No migration errors in logs

---

## 🔗 API Integration Verification

### Test Gateway Routes

```bash
# Test auth route through gateway
curl -X POST https://soccho-gateway.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'

# Expected: 200 OK or 401 Unauthorized (not 503)
```

### Test Direct Service Access

If gateway returns 503, test services directly:

```bash
# Test auth service directly
curl -i https://soccho-auth.onrender.com:8001/

# If this returns 503, service isn't running
# If this works but gateway fails, check gateway configuration
```

---

## 🐛 Common Issues & Solutions

### ❌ **503 Service Unavailable** on all endpoints

**Causes:**
1. Service not deployed/running
2. Build failed silently
3. Start command incorrect
4. Database migration error

**Solution:**
1. Check Render dashboard for service status
2. View deploy logs for errors
3. Run migrations: `python manage.py migrate`
4. Restart service from Render dashboard

---

### ❌ **502 Bad Gateway** from Render

**Causes:**
1. Service crashed during request
2. Port mismatch
3. Memory exceeded

**Solution:**
1. Check service logs for exceptions
2. Verify port configuration
3. Increase resource plan if needed

---

### ❌ **Timeout Error** from Frontend

**Causes:**
1. Service is slow (database issue)
2. Service crashed and recovering
3. Network issue

**Solution:**
1. Check database query performance
2. Monitor service health
3. Test with `curl` to isolate issue

---

## ✅ Successful Deployment Indicators

When everything is working:

- [ ] All service URLs return 200 OK or expected status
- [ ] No 503/502/504 errors
- [ ] Database migrations completed successfully
- [ ] Environment variables loaded correctly
- [ ] Render logs show no errors
- [ ] Frontend successfully connects to all services
- [ ] API calls return data, not errors

---

## 🧪 End-to-End Testing Flow

Once infrastructure is verified:

1. **Register New Account**
   ```
   Frontend: https://soccho.vercel.app
   Action: Fill register form → Submit
   Expected: Redirect to login
   Check: No 503 error, success message appears
   ```

2. **Login**
   ```
   Action: Enter credentials → Submit
   Expected: Redirect to home page
   Check: Auth token saved to localStorage
   ```

3. **Load Dashboard**
   ```
   Expected: Home page loads with user data
   Check: No API errors, data displayed correctly
   ```

4. **Add Friend**
   ```
   Action: Search and add friend
   Expected: Friend added to list
   Check: Calls social service successfully
   ```

5. **Create Transaction**
   ```
   Action: Record money given/borrowed
   Expected: Transaction saved
   Check: Calls transaction service, updates display
   ```

---

## 📊 Testing Verification Script

Save this as `test-deployment.sh`:

```bash
#!/bin/bash

echo "Testing Soccho Deployment..."

# Test Gateway
echo -n "Gateway: "
curl -s -o /dev/null -w "%{http_code}\n" https://soccho-gateway.onrender.com/health

# Test Auth Service  
echo -n "Auth Service: "
curl -s -o /dev/null -w "%{http_code}\n" https://soccho-auth.onrender.com:8001

# Test Social Service
echo -n "Social Service: "
curl -s -o /dev/null -w "%{http_code}\n" https://soccho-social.onrender.com:8002

# Test Transaction Service
echo -n "Transaction Service: "
curl -s -o /dev/null -w "%{http_code}\n" https://soccho-transaction.onrender.com:8003

# Test Frontend
echo -n "Frontend: "
curl -s -o /dev/null -w "%{http_code}\n" https://soccho.vercel.app

echo "Done!"
```

Run: `bash test-deployment.sh`

---

## 📞 Next Steps

1. ✅ Verify all services deployed on Render
2. ✅ Run database migrations
3. ✅ Set environment variables
4. ✅ Test gateway routes
5. ✅ Verify frontend connects successfully
6. ✅ Run end-to-end flow test
7. ✅ Monitor logs for errors
8. ✅ Declare production ready!

