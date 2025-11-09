# 🎯 Deployment Refactoring - Quick Reference

This document provides a quick reference for the deployment refactoring changes made to StudyBuddy.

## 📦 What Changed?

### Architecture
- **Before**: Monolithic deployment (both frontend and backend together)
- **After**: Separate deployments (Frontend on Vercel, Backend on Render)

### Backend Changes

#### 1. New Environment Variables
```bash
PORT=10000                                    # For Render (8000 for local)
CORS_ORIGINS=https://your-app.vercel.app     # Frontend URL(s)
FRONTEND_URL=https://your-app.vercel.app     # Frontend reference
```

#### 2. Updated Files
- `requirements.txt` - Added gunicorn for production
- `app/config/settings.py` - Added PORT, CORS_ORIGINS, FRONTEND_URL
- `app/main.py` - Dynamic CORS configuration, PORT from env
- `.env.template` - Updated with new variables
- `render.yaml` - Render deployment configuration (NEW)

#### 3. Key Features
- ✅ CORS accepts comma-separated origins
- ✅ PORT defaults to 10000 for Render
- ✅ Enhanced /api/health endpoint
- ✅ All routes prefixed with /api

### Frontend Changes

#### 1. New Configuration
```bash
# frontend/.env.local (NEW)
NEXT_PUBLIC_API_URL=http://localhost:8000    # For local dev
# NEXT_PUBLIC_API_URL=https://your-backend.onrender.com  # For production
```

#### 2. Updated Files
- `lib/api.ts` - Centralized axios instance (already existed)
- `next.config.ts` - Added `output: 'standalone'` for Vercel
- `vercel.json` - Vercel deployment config (NEW)
- `frontend/.env.local` - Environment variables (NEW)
- All component files - Use centralized API instead of hardcoded URLs

#### 3. Files Modified (16 total)
- `src/components/YouTubeModal.tsx`
- `src/components/GlobalChatbot.tsx`
- `src/app/peer/doubts/page.tsx`
- `src/app/peer/partners/page.tsx`
- `src/app/peer/groups/page.tsx`
- `src/app/peer/weekness/page.tsx`
- `src/app/peer/challenges/page.tsx`
- `src/app/peer/page.tsx`
- `src/app/peer/sessions/page.tsx`
- `src/app/placement/create/page.tsx`
- `src/app/placement/dashboard/page.tsx`
- `src/app/placement/practice/page.tsx`
- `src/app/placement/profiles/page.tsx`
- `src/app/placement/roadmap/page.tsx`
- `src/app/placement/test-questions/page.tsx`

### Documentation

#### New Files
1. `DEPLOYMENT.md` - Complete deployment guide (11KB)
2. `frontend/.env.local` - Frontend environment config

#### Updated Files
1. `README.md` - Added deployment section
2. `start.sh` - Updated with new environment variables

## 🚀 Quick Deployment Commands

### Deploy Backend to Render
```bash
# 1. Push to GitHub
git push origin main

# 2. In Render Dashboard:
#    - Connect repository
#    - Root directory: backend
#    - Build: pip install -r requirements.txt
#    - Start: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
#    - Add environment variables (see DEPLOYMENT.md)
```

### Deploy Frontend to Vercel
```bash
# 1. Push to GitHub
git push origin main

# 2. In Vercel Dashboard:
#    - Import repository
#    - Root directory: frontend
#    - Framework: Next.js
#    - Add NEXT_PUBLIC_API_URL environment variable
```

## 🔍 Testing Checklist

### Local Development
- [ ] Run `./start.sh` - Both servers start
- [ ] Frontend at http://localhost:3000
- [ ] Backend at http://localhost:8000
- [ ] API health check: http://localhost:8000/api/health
- [ ] Frontend can communicate with backend

### Production Deployment
- [ ] Backend health check: https://your-backend.onrender.com/api/health
- [ ] Frontend loads: https://your-app.vercel.app
- [ ] Check browser console for CORS errors (should be none)
- [ ] Test API calls from frontend to backend
- [ ] Test various features (auth, data fetching, etc.)

## ⚠️ Common Issues & Solutions

### Issue: CORS errors in browser
**Solution**: 
1. Check CORS_ORIGINS includes your Vercel URL
2. No trailing slashes in URLs
3. Redeploy backend after updating CORS_ORIGINS

### Issue: API calls return 404
**Solution**:
1. Verify NEXT_PUBLIC_API_URL is set correctly in Vercel
2. Check backend is running: visit /api/health
3. Ensure all routes are prefixed with /api

### Issue: Backend is slow (30-60 seconds)
**Solution**: This is normal for Render free tier cold starts. Options:
1. Use UptimeRobot to ping every 10 minutes
2. Upgrade to Render paid plan
3. Display loading message to users

## 📊 Environment Variables Summary

### Backend (.env)
| Variable | Local Value | Production Value |
|----------|------------|------------------|
| DATABASE_URL | `sqlite:///./exam_prep_db.db` | PostgreSQL URL or SQLite |
| PORT | `8000` | `10000` |
| CORS_ORIGINS | `http://localhost:3000` | `https://your-app.vercel.app` |
| FRONTEND_URL | `http://localhost:3000` | `https://your-app.vercel.app` |
| SECRET_KEY | `your-secret-key` | Generate new |
| GEMINI_API_KEY | `your-key` | Same |

### Frontend (.env.local)
| Variable | Local Value | Production Value |
|----------|------------|------------------|
| NEXT_PUBLIC_API_URL | `http://localhost:8000` | `https://your-backend.onrender.com` |

## 🔐 Security Checklist

- [x] No hardcoded API URLs in frontend code
- [x] Environment variables properly configured
- [x] CORS restricted to specific origins
- [x] No secrets in Git repository
- [x] .env files in .gitignore
- [x] SECRET_KEY is strong (use generator)
- [x] API keys not exposed in frontend
- [x] CodeQL security scan passed (0 alerts)

## 📝 Files Added/Modified Summary

### New Files (4)
- `render.yaml` - Render deployment config
- `vercel.json` - Vercel deployment config  
- `DEPLOYMENT.md` - Deployment guide
- `frontend/.env.local` - Frontend env vars

### Modified Files (20)
**Backend (4):**
- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/app/config/settings.py`
- `backend/.env.template`

**Frontend (16):**
- All component and page files using API calls
- `frontend/next.config.ts`

**Root (2):**
- `README.md`
- `start.sh`

## ✅ Verification Steps

1. **Code Quality**
   ```bash
   # All Python files have valid syntax ✓
   # All TypeScript files compile ✓
   # No hardcoded URLs remaining ✓
   ```

2. **Security**
   ```bash
   # CodeQL scan: 0 alerts ✓
   # No secrets in code ✓
   # Proper CORS configuration ✓
   ```

3. **Functionality**
   ```bash
   # All API routes prefixed with /api ✓
   # Centralized API instance used ✓
   # Environment variables properly configured ✓
   # Backward compatibility maintained ✓
   ```

## 🎉 Ready to Deploy!

Your application is now ready for separate deployment. Follow the complete guide in `DEPLOYMENT.md` for step-by-step instructions.

**Quick Links:**
- Backend deployment: https://dashboard.render.com
- Frontend deployment: https://vercel.com/dashboard
- Full guide: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**Need help?** Check the troubleshooting section in DEPLOYMENT.md or the README.md.
