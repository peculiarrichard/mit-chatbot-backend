# MIT Smart Chatbot - Complete Setup Guide

This is a comprehensive university chatbot system built with FastAPI, PostgreSQL, React, and OpenRouter API.

## 🚀 Features

### Student Interface
- **No Authentication Required**: Students only need to provide a username
- **User Registration**: Automatic user creation with unique identifiers
- **Student Type Detection**: Distinguishes between new and existing students
- **Chat History**: Persistent conversation history
- **Real-time Typing Indicators**: WhatsApp-like interface
- **Responsive Design**: Mobile-friendly UI

### Admin Dashboard
- **Secure Authentication**: Email/password protected admin access
- **Question Management**: View and answer unanswered student questions
- **Knowledge Base**: Manage Q&A database
- **Email Notifications**: Automatic alerts for new questions
- **Real-time Updates**: Dynamic dashboard with loading states

### Bot Intelligence
- **Contextual Responses**: Uses OpenRouter API with Claude-3-Sonnet
- **Knowledge Base Integration**: Answers from predefined Q&A database
- **Escalation System**: Unknown questions forwarded to admins
- **Learning Capability**: Continuously expanding knowledge base

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- OpenRouter API key
- Email account for SMTP (Gmail recommended)

## 🛠️ Installation Guide

### 1. Backend Setup

```bash
# Clone or create the project directory
mkdir university-chatbot
cd university-chatbot

# Create backend directory
mkdir backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your configurations
cp .env.example .env
```

### 2. Database Setup

```sql
-- Connect to PostgreSQL and create database
CREATE DATABASE university_chatbot;

-- Create a user (optional)
CREATE USER chatbot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE university_chatbot TO chatbot_user;
```

### 3. Frontend Setup

```bash
# Navigate to project root
cd ..

# Create React app
npx create-react-app frontend
cd frontend

# Install additional dependencies
npm install react-router-dom axios

# Replace package.json with provided configuration
# Copy all React components and CSS files to src/
```

### 4. Environment Configuration

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/university_chatbot
JWT_SECRET=your-very-secret-jwt-key-change-in-production
OPENROUTER_API_KEY=your-openrouter-api-key

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
ADMIN_EMAIL=admin@university.edu
```

### 5. API Keys Setup

#### OpenRouter API Key
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Create account and get API key
3. Add credits to your account
4. Add key to `.env` file

#### Gmail SMTP Setup
1. Enable 2FA on your Gmail account
2. Generate an App Password
3. Use this password in SMTP_PASSWORD

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```
Backend will run on `http://localhost:8000`

### Start Frontend Server
```bash
cd frontend
npm start
```
Frontend will run on `http://localhost:3000`

## 📊 Database Schema

The system automatically creates these tables:

- **users**: Student information and identifiers
- **admins**: Admin authentication
- **messages**: Chat history
- **qa_entries**: Knowledge base
- **unanswered_questions**: Questions pending admin review
