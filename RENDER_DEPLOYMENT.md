# Render.com Deployment Guide (Backend)

## 🚀 Complete Step-by-Step Instructions

### **STEP 1: Sign Up on Render.com**
1. Go to https://render.com
2. Click **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub account
5. Click **"Authorize render"**

---

### **STEP 2: Create a New Web Service**

1. After login, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see your GitHub repositories in a list
4. Find **movie-app** repository
5. Click **"Connect"** next to it

---

### **STEP 3: Configure Your Service**

Fill in the following settings:

#### **Basic Settings:**
- **Name**: `movie-app-backend` (or any name you like)
- **Runtime**: `Python 3` (auto-selected)
- **Region**: `us-east` (default is fine)
- **Branch**: `main`

#### **Build & Deploy:**
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**: 
  ```
  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
  ```

#### **Environment Variables:**
Click **"Add Environment Variable"** and add:

| Key | Value |
|-----|-------|
| `PYTHONUNBUFFERED` | `1` |
| `DATABASE_URL` | `sqlite:///./userdb.db` |

#### **Plan Type:**
- Select **"Free"** (to start)
  - Note: Free tier has limitations (pauses after 15 mins of inactivity)
  - Upgrade to **"Starter"** ($7/month) if you want 24/7 uptime

---

### **STEP 4: Deploy**

1. All fields filled? Click **"Create Web Service"** (bottom right)
2. Render will start building:
   - First build takes 2-3 minutes
   - You'll see logs on screen
   - Wait for: **"Your service is live"** message

---

### **STEP 5: Get Your Backend URL**

1. Once deployed, go to your service dashboard
2. At the top, you'll see a URL like:
   ```
   https://movie-app-backend.onrender.com
   ```
3. **Copy this URL** - you'll need it for the frontend!

---

## ✅ Verify Backend is Working

Test your API in a browser:

```
https://your-service-name.onrender.com/
```

You should see:
```json
{"message":"App running 🚀"}
```

Try the movies endpoint:
```
https://your-service-name.onrender.com/movies
```

Should return a list of movies!

---

## 📝 Update Frontend with Backend URL

Now that you have your backend URL, update your frontend files:

### **Files to Update:**
1. `frontend/login.html`
2. `frontend/index.html`
3. `frontend/admin.html`

### **What to Change:**

Find all occurrences of:
```javascript
fetch("http://127.0.0.1:8000/
```

Replace with:
```javascript
fetch("https://your-backend-url.onrender.com/
```

**Example:**

**Before:**
```javascript
fetch("http://127.0.0.1:8000/login", {
```

**After:**
```javascript
fetch("https://movie-app-backend.onrender.com/login", {
```

---

## 🔧 Troubleshooting Common Issues

### **Issue: "Build failed"**
- Check `requirements.txt` exists
- Make sure all imports are listed in requirements.txt
- Look at build logs for specific error

### **Issue: "Service crashes after deployment"**
- Check Start Command is correct
- Look at logs: see what error occurred
- Make sure database.py is correct

### **Issue: API returns 500 error**
- Check backend logs in Render dashboard
- Look for Python exceptions
- Verify database path is correct

### **Issue: Frontend can't connect to backend**
- Verify you updated the fetch URLs correctly
- Check CORS is enabled in `backend/main.py`
- Make sure backend URL has no trailing slash

---

## 📊 Monitor Your Backend

After deployment:

1. Go to your Render dashboard
2. Click your service name
3. View **"Logs"** tab to see requests and errors
4. View **"Metrics"** tab to see CPU/Memory usage
5. **"Settings"** tab to update environment variables

---

## 💰 Cost Considerations

| Plan | Cost | Uptime | Good For |
|------|------|--------|----------|
| **Free** | $0 | Pauses after 15 mins | Testing |
| **Starter** | $7/month | 24/7 | Small projects |
| **Standard** | $25/month | 24/7 + more resources | Production |

**Tip:** Free tier is fine for testing. Upgrade to Starter when going live!

---

## 🔐 Keep Backend Secrets Safe

**DON'T** add sensitive data in environment variables visible to frontend:
- ✅ Database URL (public)
- ❌ API Keys (never!)
- ❌ Passwords (never!)

For TMDB API key in `backend/main.py`:
```python
API_KEY = os.getenv("TMDB_API_KEY", "your-test-key")
```

---

## 📤 After Deployment

1. ✅ Backend deployed on Render
2. ⏭️ Next: Deploy **frontend on Netlify**
3. ⏭️ Then: Connect them together

---

## 🆘 Need Help?

If deployment fails:
1. Check the **Logs** tab in Render dashboard
2. Look for the red error message
3. Check `requirements.txt` is in root directory
4. Verify `backend/main.py` exists

**Common error fixes:**
- ModuleNotFoundError → Missing from requirements.txt
- SyntaxError → Check Python code
- OperationalError → Database issue, check database.py

---

## Quick Command to Push Updates

After you make changes:
```bash
git add .
git commit -m "Update changes"
git push origin main
```

**Render auto-redeploys** when you push to GitHub! 🚀

---

**Ready to deploy the frontend?** Follow the Netlify guide next!
