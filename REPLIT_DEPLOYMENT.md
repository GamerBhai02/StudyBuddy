# 🚀 Deploying StudyBuddy on Replit

This guide will help you deploy StudyBuddy on Replit in just a few minutes!

## 📋 What You'll Need

- A Replit account (free tier works!)
- API keys for AI services (Mistral, Groq, or Google GenAI)

## 🎯 Step-by-Step Deployment

### Step 1: Import the Repository

1. Go to [Replit.com](https://replit.com)
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Paste the repository URL: `https://github.com/GamerBhai02/StudyBuddy`
5. Click "Import from GitHub"

### Step 2: Automatic Setup

Once imported, Replit will automatically:
- ✅ Detect the `.replit` configuration
- ✅ Install Node.js 20 and Python 3.11
- ✅ Set up the Nix environment
- ✅ Prepare the startup script

### Step 3: Run the Application

1. Click the green "Run" button at the top
2. Wait for the installation process (first time takes 2-3 minutes)
3. You'll see:
   ```
   🚀 Starting StudyBuddy Application...
   📦 Installing Backend Dependencies...
   ✓ Backend dependencies installed
   🗄️  Initializing Database...
   ✓ Database initialized
   🔧 Starting Backend Server...
   ✓ Backend running on http://0.0.0.0:8000
   📦 Installing Frontend Dependencies...
   ✓ Frontend dependencies installed
   🎨 Starting Frontend Server...
   ✓ Frontend running on http://0.0.0.0:3000
   ```

### Step 4: Configure API Keys

1. In the Replit file explorer, open `backend/.env`
2. Replace the placeholder values with your actual API keys:
   ```env
   DATABASE_URL=sqlite:///./studybuddy.db
   SECRET_KEY=your-secret-key-change-this-in-production
   MISTRAL_API_KEY=your-actual-mistral-key
   GROQ_API_KEY=your-actual-groq-key
   GOOGLE_API_KEY=your-actual-google-key
   ```
3. Click "Stop" (the square button)
4. Click "Run" again

### Step 5: Access Your Application

- **Frontend**: Click the window icon at the top right or use the webview tab
- **Backend API**: Add `:8000` to your Repl URL
- **API Documentation**: Add `:8000/docs` to your Repl URL

Your Repl URL will look like: `https://your-repl-name.your-username.repl.co`

## 🔧 How It Works

### Architecture on Replit

```
Replit Container
├── Backend (Port 8000)
│   ├── FastAPI Server
│   ├── SQLite Database
│   └── AI Services
│
└── Frontend (Port 3000)
    ├── Next.js Server
    └── React Application
```

### Files Involved

1. **`.replit`** - Main configuration file
   - Defines the run command
   - Sets up environment variables
   - Configures ports (3000 for frontend, 8000 for backend)

2. **`replit.nix`** - System dependencies
   - Node.js 20
   - Python 3.11
   - PostgreSQL (optional, using SQLite by default)
   - npm, pip, typescript

3. **`start.sh`** - Startup script
   - Creates environment files if missing
   - Installs dependencies
   - Initializes database
   - Starts both servers concurrently

## 🎛️ Configuration Options

### Database

By default, the app uses SQLite on Replit (simpler for deployment). To use PostgreSQL:

1. Enable the PostgreSQL database in Replit
2. Update `backend/.env`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/studybuddy
   ```

### Environment Variables

You can also set environment variables in Replit's "Secrets" panel:

1. Click the lock icon in the left sidebar
2. Add keys:
   - `MISTRAL_API_KEY`
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY`
   - `SECRET_KEY`

The app will automatically use these if found.

## 🐛 Troubleshooting

### Issue: "Port 3000 is already in use"

**Solution**: Click "Stop" and then "Run" again. This kills any hanging processes.

### Issue: Frontend not loading

**Solution**: 
1. Check the console for errors
2. Ensure `frontend/.env.local` has the correct API URL
3. Try accessing via the direct URL (click the window icon)

### Issue: Backend errors with AI responses

**Solution**: 
1. Verify API keys in `backend/.env`
2. Check that keys have no extra spaces
3. Ensure you have credits/quota on your AI service accounts

### Issue: Database errors

**Solution**:
1. In the Shell tab, run:
   ```bash
   cd backend
   rm studybuddy.db
   python init_db.py
   ```
2. Click "Run" again

### Issue: Dependencies not installing

**Solution**:
1. Click "Stop"
2. In Shell tab:
   ```bash
   cd frontend && npm install
   cd ../backend && pip install -r requirements.txt
   ```
3. Click "Run"

## 📊 Resource Usage

### Free Tier Limits
- ✅ Adequate for development and testing
- ✅ Handles multiple concurrent users
- ⚠️ May sleep after inactivity (Replit free tier)

### Hacker Tier Benefits
- ⚡ Always-on (no sleeping)
- 🚀 Better performance
- 💾 More storage
- 🔒 Private Repls

## 🔄 Updating Your Deployment

When new changes are pushed to the repository:

1. In Replit, open the Shell tab
2. Run:
   ```bash
   git pull origin main
   ```
3. Click "Run" to restart with updates

## 🌐 Custom Domain

To use a custom domain:

1. Upgrade to Replit Hacker tier
2. Go to your Repl settings
3. Add your custom domain
4. Update DNS records as instructed

## 💡 Tips for Best Performance

1. **Keep API Keys Secure**: Use Replit Secrets instead of `.env` for production
2. **Monitor Logs**: Check the console regularly for errors
3. **Use SQLite for Small Apps**: It's simpler and requires no setup
4. **Upgrade Database**: For heavy usage, switch to PostgreSQL
5. **Enable Always-On**: For production, use Hacker tier to prevent sleeping

## 🎉 Success!

Once running, you should see:
- ✅ Frontend at your Repl URL
- ✅ Backend API at URL:8000
- ✅ API docs at URL:8000/docs
- ✅ All features working (chatbot, practice, etc.)

## 📚 Next Steps

1. Test all features:
   - Create a study plan
   - Try the AI chatbot
   - Generate practice questions
   - Explore peer learning

2. Share your Repl:
   - Click the share button
   - Invite collaborators
   - Or make it public

3. Monitor usage:
   - Check the console for any errors
   - Monitor API quota usage
   - Track user activity

---

**Need Help?** 
- Check Replit's documentation: https://docs.replit.com
- Open an issue on GitHub
- Join the Replit Discord community

Happy Learning! 🎓✨
