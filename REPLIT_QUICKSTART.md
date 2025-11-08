# ⚡ Quick Replit Setup

## 🚀 3-Step Deployment

### Step 1: Import
```
1. Go to replit.com
2. Click "Import from GitHub"
3. Paste: https://github.com/GamerBhai02/StudyBuddy
```

### Step 2: Run
```
Click the green "Run" button
Wait 2-3 minutes for first-time setup
```

### Step 3: Configure
```
Edit backend/.env with your API keys:
- MISTRAL_API_KEY
- GROQ_API_KEY
- GOOGLE_API_KEY

Click Stop, then Run again
```

## ✅ That's It!

- **Frontend**: Click "Open website" button
- **Backend API**: Add `:8000` to your Repl URL
- **API Docs**: Add `:8000/docs` to your Repl URL

## 🔧 Files You'll See

- `.replit` - Tells Replit how to run
- `replit.nix` - System dependencies
- `start.sh` - Starts both servers
- `REPLIT_DEPLOYMENT.md` - Full guide

## 🐛 Quick Fixes

**Not working?** 
1. Click Stop
2. Click Run again

**Still not working?**
```bash
cd backend && python init_db.py
cd ../frontend && npm install
```
Then click Run

## 📋 Default Credentials

The app uses a default user for testing:
- Email: `student@studybuddy.com`
- User ID: 1

## 🎯 What Works Out of the Box

✅ Both frontend and backend
✅ SQLite database (no setup needed)
✅ All AI features (add your keys)
✅ File uploads
✅ Practice questions
✅ Chatbot with voice
✅ Peer learning
✅ Placement prep

## 💡 Pro Tips

1. **Secrets**: Use Replit Secrets (lock icon) instead of .env for API keys
2. **Always On**: Upgrade to Hacker tier to prevent sleeping
3. **Database**: SQLite is perfect for learning, PostgreSQL for production
4. **Debugging**: Check the Console tab for errors

---

**Full Documentation**: See REPLIT_DEPLOYMENT.md
**Issues?** Check troubleshooting section in the full guide
