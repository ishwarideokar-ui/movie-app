# Movie App Deployment Guide

## 🚀 Deployment Options

### Option 1: FREE & EASY - Render.com + Netlify (Recommended for Beginners)

#### Backend Deployment (Render.com)

1. **Create Git Repository** (if not already done):
```bash
cd c:\Users\Lenovo\OneDrive\Desktop\movie--app
git init
git add .
git commit -m "Initial commit"
```

2. **Push to GitHub**:
   - Create account at github.com
   - Create new repository
   - Push your code: `git push origin main`

3. **Deploy Backend on Render.com**:
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: movie-app-backend
     - **Runtime**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0`
     - **Environment Variables**:
       ```
       DATABASE_URL=sqlite:///./userdb.db
       ```
   - Deploy (Free tier available)

4. **Get Backend URL**: 
   - Render will give you URL like: `https://movie-app-backend.onrender.com`

#### Frontend Deployment (Netlify)

1. **Update API URLs in Frontend**:
   - Edit `frontend/login.html`, `frontend/index.html`, `frontend/admin.html`
   - Replace `http://127.0.0.1:8000` with your Render backend URL:
   ```javascript
   fetch("https://movie-app-backend.onrender.com/login", {
   ```

2. **Deploy on Netlify**:
   - Go to https://netlify.com
   - Sign up with GitHub
   - Click "Add new site" → "Import an existing project"
   - Select your repository
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: (leave empty - static site)
     - **Publish directory**: `frontend`
   - Deploy

3. **Get Frontend URL**: Netlify will provide your live site URL

---

### Option 2: PROFESSIONAL - Railway.app (Recommended for Production)

1. **Navigate to [Railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Create New Project**
4. **Add GitHub Repository**
5. **Configure Service**:
   - Python environment detected automatically
   - Add environment variable: `DATABASE_URL=sqlite:///./userdb.db`
6. **Deploy & Get URL**

---

### Option 3: DOCKER - Deploy Anywhere

#### Create Docker Configuration

1. **Create `Dockerfile`** in project root:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create `docker-compose.yml`**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///./userdb.db
```

3. **Build & Run**:
```bash
docker-compose up --build
```

---

### Option 4: HEROKU (Traditional Cloud Deployment)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Create `Procfile`** in project root:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

3. **Create `requirements.txt`**:
```bash
pip freeze > requirements.txt
```

4. **Deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

---

### Option 5: Your Own Server (VPS)

#### Using DigitalOcean, AWS EC2, or Linode

1. **SSH into server**:
```bash
ssh root@your_server_ip
```

2. **Install dependencies**:
```bash
apt update && apt install python3-pip python3-venv nodejs
```

3. **Clone your repository**:
```bash
git clone https://github.com/your-username/movie-app.git
cd movie-app
```

4. **Setup backend**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn supervisor
```

5. **Setup Nginx** (reverse proxy):
```bash
apt install nginx
# Configure nginx to proxy requests to 127.0.0.1:8000
```

6. **Use Supervisor for auto-restart**:
```bash
# Create supervisor config for background processes
```

---

## 📋 Pre-Deployment Checklist

### 1. Create `requirements.txt`:
```bash
pip freeze > requirements.txt
```

**Or manually create it with:**
```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
requests==2.31.0
sqlalchemy==2.0.23
python-multipart==0.0.6
```

### 2. Create `.gitignore`:
```
__pycache__/
*.pyc
*.db
*.sqlite
.env
venv/
.DS_Store
```

### 3. Environment Variables:
Create `.env` file (don't commit this):
```
API_KEY=533d900aa6f08eb65ad4bcbc91bd71d3
DATABASE_URL=sqlite:///./userdb.db
```

### 4. Update CORS for Production:
In `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔗 Update Frontend API Endpoints

Create a config file `frontend/config.js`:
```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:8000' 
    : 'https://your-backend-url.com';

export default API_URL;
```

Then update all fetch calls to use this config.

---

## 📊 Recommended Deployment Stack

| Component | Service | Free Tier | Ease |
|-----------|---------|-----------|------|
| **Backend** | Render.com | ✅ Yes (Paused after inactivity) | ⭐⭐⭐ |
| **Frontend** | Netlify | ✅ Yes (Unlimited) | ⭐⭐⭐ |
| **Database** | SQLite (on backend) | ✅ Yes | ⭐⭐ |
| **Custom Domain** | Namecheap | 💰 $12-15/year | ⭐⭐ |

---

## 🚨 Important Notes

1. **SQLite Limitations**: SQLite works for small apps but use PostgreSQL for production
2. **Static Files**: Frontend HTML files should be served separately from backend API
3. **Environment Variables**: Keep sensitive data in environment variables, not in code
4. **HTTPS Required**: Always use HTTPS in production (free with Netlify/Render)
5. **CORS Configuration**: Update allowed origins for your production domains

---

## Quick Start Deployment Commands

### For Render.com:
```bash
git init
git add .
git commit -m "Ready for deployment"
git push origin main
# Then connect on Render dashboard
```

### For Docker:
```bash
docker build -t movie-app .
docker run -p 8000:8000 movie-app
```

### For Local Production:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🎯 Next Steps

1. Choose your deployment platform
2. Create `requirements.txt` and `.gitignore`
3. Push code to GitHub
4. Connect to chosen platform
5. Update frontend API URLs
6. Test all features
7. Monitor logs and performance

Need help with any specific platform? Let me know!
