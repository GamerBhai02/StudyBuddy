# 🎓 Smart Study Buddy

An AI-powered comprehensive study platform that helps students prepare for both academic exams and job placement interviews. Built with Next.js, FastAPI, and powered by advanced LLM technology.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-16.0-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-19.2-blue)

## ✨ Features

### 🎯 Exam Preparation (Phases 1-3)
- **AI-Powered Study Plans**: Generate personalized study schedules based on your exam date and syllabus
- **Smart Practice Sessions**: MCQ and written questions with instant AI feedback
- **Progress Tracking**: Comprehensive dashboard to monitor your learning journey
- **Spaced Repetition**: Intelligent review scheduling for optimal retention
- **Weak Topic Analysis**: Identify and focus on areas that need improvement
- **Exam Day Preparation**: Last-minute revision and confidence boost features
- **Voice-Enabled Chatbot**: Interactive AI assistant with text-to-speech capabilities

### 💼 Placement Preparation (Phase 4)
- **Company-Specific Plans**: Tailored preparation roadmaps for top tech companies (Google, Amazon, Microsoft, etc.)
- **Round-Wise Preparation**: Structured guidance for aptitude, coding, and interview rounds
- **DSA Practice**: Data structures and algorithms questions with difficulty progression
- **System Design**: Learn and practice system design concepts
- **Mock Interviews**: Simulate real interview experiences

### 👥 Peer Learning
- **Study Groups**: Form and join study groups with peers
- **Doubt Resolution**: Ask and answer questions within the community
- **Study Partners**: Find and connect with study partners
- **Group Challenges**: Participate in collaborative learning challenges
- **Study Sessions**: Schedule and track group study sessions

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16.0 with React 19.2
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.1
- **State Management**: Zustand
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Form Handling**: React Hook Form

### Backend
- **Framework**: FastAPI 0.104
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **File Processing**: PyPDF2 for document extraction
- **AI/LLM**: Multi-provider support (Mistral, Groq, Google GenAI)
- **Server**: Uvicorn

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- PostgreSQL (v14 or higher)
- npm or yarn package manager
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/GamerBhai02/StudyBuddy.git
cd StudyBuddy
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file in the backend directory with:
# DATABASE_URL=postgresql://username:password@localhost:5432/studybuddy
# SECRET_KEY=your-secret-key-here
# Add your AI API keys (Mistral, Groq, Google GenAI)

# Initialize the database
python init_db.py

# Run database migrations (if needed)
python migrate.py

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
API documentation will be at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
# Create a .env.local file in the frontend directory with:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start the development server
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
StudyBuddy/
├── frontend/                    # Next.js frontend application
│   ├── src/
│   │   ├── app/                # Next.js app directory
│   │   │   ├── dashboard/      # Dashboard pages
│   │   │   ├── exam-day/       # Exam day preparation
│   │   │   ├── onboarding/     # Onboarding flow
│   │   │   ├── peer/           # Peer learning features
│   │   │   ├── placement/      # Placement preparation
│   │   │   ├── practice/       # Practice sessions
│   │   │   └── lesson/         # Lesson pages
│   │   ├── components/         # Reusable React components
│   │   └── lib/                # Utilities and API clients
│   ├── public/                 # Static assets
│   └── package.json
│
├── backend/                     # FastAPI backend application
│   ├── app/
│   │   ├── data/               # Static data (companies, resources)
│   │   ├── models/             # Database models
│   │   ├── routes/             # API routes
│   │   ├── services/           # Business logic
│   │   └── main.py             # Application entry point
│   ├── uploads/                # Uploaded files storage
│   ├── requirements.txt        # Python dependencies
│   └── init_db.py              # Database initialization
│
└── README.md                    # This file
```

## 🎮 Usage Guide

### For Exam Preparation:

1. **Create a Study Plan**
   - Click on "Exam Preparation" from the home page
   - Upload your syllabus (PDF format)
   - Set your exam date
   - Let AI generate a personalized study plan

2. **Daily Study**
   - Check your dashboard for today's tasks
   - Complete practice sessions
   - Review weak topics
   - Track your progress

3. **Practice & Review**
   - Access practice questions for any topic
   - Get instant AI feedback
   - Follow spaced repetition schedule
   - Use exam day prep for last-minute revision

### For Placement Preparation:

1. **Select Target Company**
   - Choose from top tech companies
   - Set your interview date
   - Get a customized preparation roadmap

2. **Follow the Roadmap**
   - Complete aptitude round preparation
   - Practice DSA problems
   - Study system design concepts
   - Prepare for HR rounds

3. **Track Progress**
   - Monitor completion of each phase
   - Practice with difficulty progression
   - Review weak areas

## 🤖 AI Chatbot

The platform includes a global AI chatbot with:
- Context-aware responses based on current page
- Voice input (speech-to-text)
- Voice output (text-to-speech) with customizable settings
- Support for multiple voice profiles
- Quick question suggestions

## 🔐 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost:5432/studybuddy
SECRET_KEY=your-secret-key-here
MISTRAL_API_KEY=your-mistral-api-key
GROQ_API_KEY=your-groq-api-key
GOOGLE_API_KEY=your-google-api-key
```

## 📝 Development

### Running Linters

```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend
# Add your Python linting commands
```

### Building for Production

```bash
# Frontend
cd frontend
npm run build
npm start

# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **GamerBhai02** - *Initial work* - [GitHub Profile](https://github.com/GamerBhai02)

## 🙏 Acknowledgments

- Next.js team for the amazing framework
- FastAPI for the high-performance backend framework
- OpenAI, Mistral, Groq, and Google for AI capabilities
- All contributors who have helped shape this project

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation at `/docs` endpoint of the API

## 🗺️ Roadmap

- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Real-time collaborative study sessions
- [ ] Integration with more learning platforms
- [ ] Advanced AI tutoring features
- [ ] Gamification and achievement system

---

Made with ❤️ for students, by students
