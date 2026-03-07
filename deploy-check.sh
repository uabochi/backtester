#!/bin/bash
# Render Deployment Preparation Script

echo "🚀 Preparing Backtester for Render Deployment"

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📦 Checking backend dependencies..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found in backend/"
    exit 1
fi

echo "📦 Checking frontend dependencies..."
cd ../frontend
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found in frontend/"
    exit 1
fi

echo "✅ Project structure looks good!"
echo ""
echo "📋 Deployment Checklist:"
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repo to Render"
echo "3. Create two services:"
echo "   a) Backend Web Service (Python)"
echo "   b) Frontend Static Site"
echo "4. Set environment variables:"
echo "   - Frontend: VITE_API_URL=https://your-backend-service.onrender.com"
echo ""
echo "🔗 Useful links:"
echo "- Render Dashboard: https://dashboard.render.com"
echo "- Render Docs: https://docs.render.com"