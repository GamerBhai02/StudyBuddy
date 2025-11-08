#!/bin/bash

echo "🚀 Starting StudyBuddy Application..."
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env files exist, if not create templates
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Creating backend/.env template...${NC}"
    cat > backend/.env << 'EOF'
DATABASE_URL=sqlite:///./studybuddy.db
SECRET_KEY=your-secret-key-change-this-in-production
MISTRAL_API_KEY=your-mistral-api-key
GROQ_API_KEY=your-groq-api-key
GOOGLE_API_KEY=your-google-api-key
EOF
    echo -e "${GREEN}✓ Backend .env template created${NC}"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo -e "${YELLOW}Creating frontend/.env.local...${NC}"
    cat > frontend/.env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo -e "${GREEN}✓ Frontend .env.local created${NC}"
fi

# Install Backend Dependencies
echo -e "\n${BLUE}📦 Installing Backend Dependencies...${NC}"
cd backend
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Backend dependency installation had warnings${NC}"
fi

# Initialize Database
echo -e "\n${BLUE}🗄️  Initializing Database...${NC}"
python init_db.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${YELLOW}⚠ Database may already exist${NC}"
fi

# Start Backend Server
echo -e "\n${BLUE}🔧 Starting Backend Server...${NC}"
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend running on http://0.0.0.0:8000 (PID: $BACKEND_PID)${NC}"

# Give backend a moment to start
sleep 3

# Install Frontend Dependencies
echo -e "\n${BLUE}📦 Installing Frontend Dependencies...${NC}"
cd ../frontend
npm install --silent
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Frontend dependency installation had warnings${NC}"
fi

# Start Frontend Server
echo -e "\n${BLUE}🎨 Starting Frontend Server...${NC}"
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend running on http://0.0.0.0:3000 (PID: $FRONTEND_PID)${NC}"

# Print access information
echo -e "\n${GREEN}======================================"
echo -e "✅ StudyBuddy is now running!"
echo -e "======================================${NC}"
echo -e "${BLUE}📱 Frontend:${NC} http://0.0.0.0:3000"
echo -e "${BLUE}🔌 Backend API:${NC} http://0.0.0.0:8000"
echo -e "${BLUE}📚 API Docs:${NC} http://0.0.0.0:8000/docs"
echo -e "\n${YELLOW}Note: Update the .env files with your actual API keys${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
