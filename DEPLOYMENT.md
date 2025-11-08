# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying the StudyBuddy application with a separate frontend (Vercel) and backend (Render).

## 📋 Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐
│  Vercel (Free)  │         │  Render (Free)   │
│                 │         │                  │
│  Next.js        │  HTTP   │  FastAPI         │
│  Frontend       │ ◄─────► │  Backend         │
│                 │  CORS   │                  │
└─────────────────┘         └──────────────────┘
                                    │
                                    ▼
                            ┌──────────────────┐
                            │  PostgreSQL or   │
                            │  SQLite          │
                            └──────────────────┘
```

## 🎯 Prerequisites

Before you begin, ensure you have:
- A GitHub account
- A Vercel account (sign up at [vercel.com](https://vercel.com))
- A Render account (sign up at [render.com](https://render.com))
- API keys for AI services (Gemini, Mistral, Groq)

## 🔧 Part 1: Deploy Backend to Render

### Step 1: Prepare Your Backend

1. **Fork/Clone this repository** to your GitHub account

2. **Verify your backend files** are in the `backend/` directory with:
   - `requirements.txt`
   - `app/main.py`
   - `.env.template`

### Step 2: Create a New Web Service on Render

1. **Log in to Render** at [dashboard.render.com](https://dashboard.render.com)

2. **Click "New +"** and select **"Web Service"**

3. **Connect your GitHub repository**:
   - Click "Connect account" if not already connected
   - Select your StudyBuddy repository

4. **Configure the service**:
   - **Name**: `studybuddy-backend` (or your preferred name)
   - **Region**: Choose closest to your users (e.g., Oregon)
   - **Branch**: `main` (or your production branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Select **"Free"** (includes 750 hours/month)

5. **Click "Advanced"** and add environment variables:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `PORT` | `10000` | Render uses this automatically |
   | `DATABASE_URL` | `sqlite:///./exam_prep_db.db` | Or PostgreSQL URL if using a database |
   | `SECRET_KEY` | Click "Generate" | For JWT tokens |
   | `GEMINI_API_KEY` | `your-gemini-key` | Get from [Google AI](https://makersuite.google.com/app/apikey) |
   | `MISTRAL_API_KEY` | `your-mistral-key` | Optional: Get from [Mistral](https://console.mistral.ai/) |
   | `GROQ_API_KEY` | `your-groq-key` | Optional: Get from [Groq](https://console.groq.com/) |
   | `GOOGLE_API_KEY` | `your-google-key` | For additional features |
   | `CORS_ORIGINS` | `https://your-app.vercel.app` | Update after deploying frontend |
   | `FRONTEND_URL` | `https://your-app.vercel.app` | Update after deploying frontend |
   | `ALGORITHM` | `HS256` | JWT algorithm |

6. **Click "Create Web Service"**

7. **Wait for deployment** (5-10 minutes for first deploy)

8. **Note your backend URL**: It will be like `https://studybuddy-backend.onrender.com`

9. **Test the health endpoint**: Visit `https://your-backend-url.onrender.com/api/health`
   - You should see: `{"status": "healthy", "phase": "3", "features": [...]}`

### Step 3: Update CORS Settings

After deploying the frontend (next section), return here to update:

1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Update `CORS_ORIGINS` to include your Vercel URL:
   ```
   https://your-app.vercel.app,http://localhost:3000
   ```
5. Update `FRONTEND_URL` to your Vercel URL:
   ```
   https://your-app.vercel.app
   ```
6. Click "Save Changes"

### ⚠️ Important Notes about Render Free Tier

- **Cold Starts**: Free tier services spin down after 15 minutes of inactivity
- **First request** after inactivity may take 30-60 seconds to respond
- **Sleep behavior**: This is normal for free tier
- **Workaround**: Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your API every 10 minutes
- **Database**: SQLite works but data may be lost on redeploy. Use external PostgreSQL for persistence.

## 🌐 Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Your Frontend

1. **Verify your frontend files** are in the `frontend/` directory with:
   - `package.json`
   - `next.config.ts`
   - `src/` directory with your components

### Step 2: Deploy to Vercel

1. **Log in to Vercel** at [vercel.com](https://vercel.com)

2. **Click "Add New..."** and select **"Project"**

3. **Import your Git repository**:
   - Click "Import Git Repository"
   - Select your StudyBuddy repository
   - Click "Import"

4. **Configure the project**:
   - **Framework Preset**: `Next.js` (should auto-detect)
   - **Root Directory**: `frontend` (click "Edit" and select it)
   - **Build Command**: `npm run build` (default is fine)
   - **Output Directory**: `.next` (default is fine)
   - **Install Command**: `npm install` (default is fine)

5. **Add Environment Variables**:
   - Click "Environment Variables"
   - Add the following:
     
     | Key | Value |
     |-----|-------|
     | `NEXT_PUBLIC_API_URL` | `https://your-backend.onrender.com` |
   
   - Replace `your-backend.onrender.com` with your actual Render backend URL

6. **Click "Deploy"**

7. **Wait for deployment** (2-5 minutes)

8. **Note your frontend URL**: It will be like `https://studybuddy-abc123.vercel.app`

### Step 3: Update Backend CORS

Now that you have your Vercel URL:

1. Return to **Render dashboard**
2. Update the `CORS_ORIGINS` environment variable (as described in Part 1, Step 3)
3. Save and wait for the backend to redeploy

### Step 4: Test Your Application

1. Visit your Vercel URL
2. Try creating an account or logging in
3. Test various features to ensure frontend-backend communication works

## 🗄️ Part 3: Database Setup (Optional - PostgreSQL)

If you want persistent data and better performance, set up PostgreSQL:

### On Render:

1. **Create a PostgreSQL database**:
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Choose a name: `studybuddy-db`
   - Choose free plan
   - Click "Create Database"

2. **Copy the Internal Database URL**:
   - Find the "Internal Database URL" in database info
   - It looks like: `postgresql://user:pass@hostname/dbname`

3. **Update backend environment variable**:
   - Go to your web service
   - Update `DATABASE_URL` with the internal URL
   - Save changes

4. **Run database migrations**:
   - The application will automatically create tables on first run
   - Alternatively, you can run migrations manually via Render Shell

## 🔄 Part 4: Continuous Deployment

Both Vercel and Render support automatic deployments:

### Automatic Deployments:

- **Vercel**: Automatically deploys on every push to your main branch
- **Render**: Automatically deploys on every push to your main branch

### Manual Deployments:

- **Vercel**: Go to project → Deployments → click "Redeploy"
- **Render**: Go to web service → Manual Deploy → click "Deploy"

## 🔍 Troubleshooting

### Frontend shows "Network Error" or "Connection Refused"

**Solution**:
1. Check that `NEXT_PUBLIC_API_URL` is correctly set in Vercel
2. Ensure the URL includes `https://` and no trailing slash
3. Verify backend is running: visit `https://your-backend.onrender.com/api/health`

### Backend shows 403 CORS errors in browser console

**Solution**:
1. Check `CORS_ORIGINS` includes your Vercel URL
2. Ensure CORS_ORIGINS format: `https://your-app.vercel.app,http://localhost:3000`
3. No trailing slashes in CORS origins
4. Redeploy backend after updating CORS settings

### Backend responds slowly (30-60 seconds) on first request

**Normal behavior** for Render free tier cold starts.

**Solutions**:
- Upgrade to paid plan ($7/month)
- Use UptimeRobot to ping every 10 minutes
- Display a loading message to users

### Database data disappears after redeploy

**Cause**: SQLite is ephemeral on Render free tier.

**Solution**: Use external PostgreSQL database (see Part 3)

### API Keys not working

**Check**:
1. Environment variables are set correctly (no extra spaces)
2. API keys are valid and active
3. Check Render logs for specific API errors: Dashboard → Logs

### Build fails on Vercel

**Common issues**:
1. Wrong root directory - should be `frontend`
2. Missing dependencies - run `npm install` locally first
3. TypeScript errors - fix in development before deploying

### Build fails on Render

**Common issues**:
1. Wrong root directory - should be `backend`
2. Missing Python packages - verify `requirements.txt`
3. Python version issues - Render uses Python 3.7+

## 📊 Monitoring Your Deployment

### Check Backend Status:
```bash
curl https://your-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "phase": "3",
  "features": ["chatbot", "practice", "exam-day"]
}
```

### Check Frontend Status:
Visit your Vercel URL and check browser console for any errors.

### View Logs:

- **Render Logs**: Dashboard → Your Service → Logs
- **Vercel Logs**: Dashboard → Your Project → Deployments → View Function Logs

## 🆓 Free Tier Limitations

| Service | Limitation | Impact |
|---------|-----------|--------|
| Render Free | 750 hours/month | Enough for one service running 24/7 |
| Render Free | Spins down after 15min inactive | First request may be slow |
| Render Free | No persistent disk | Use external database |
| Vercel Free | 100GB bandwidth/month | Enough for small to medium apps |
| Vercel Free | 100 hours build time/month | Plenty for most projects |

## 🔐 Security Best Practices

1. **Never commit `.env` files** to Git
2. **Use strong SECRET_KEY** - generate with: 
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
3. **Keep API keys secret** - never expose in frontend code
4. **Use HTTPS only** in production (automatic with Vercel/Render)
5. **Regularly rotate** API keys and secrets

## 🎉 Success!

Your StudyBuddy application should now be live on:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.onrender.com`

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## 💡 Tips for Production

1. **Use a custom domain** on Vercel (free with Vercel)
2. **Enable Vercel Analytics** for usage insights
3. **Set up error tracking** (Sentry, LogRocket)
4. **Monitor uptime** (UptimeRobot, Pingdom)
5. **Backup your database** regularly if using PostgreSQL

---

Need help? Check the [troubleshooting section](#troubleshooting) or open an issue on GitHub!
