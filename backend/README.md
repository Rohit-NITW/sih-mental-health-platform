# Harmony AI Chatbot Integration

This directory contains the backend server for the Harmony AI Chatbot that has been integrated into your student dashboard.

## Features

🤖 **Mental Health Focused AI**: Specifically designed for student mental health support  
💬 **Conversational Interface**: Natural chat experience with context retention  
🚨 **Crisis Detection**: Automatically detects crisis keywords and provides appropriate resources  
🎓 **Student-Centric**: Addresses academic stress, social anxiety, and student-specific challenges  
🔒 **Privacy Focused**: Conversations are session-based and not permanently stored  

## Quick Setup

### Option 1: Automated Setup (Recommended)
1. Double-click `setup_and_run.bat`
2. The script will install dependencies and start the server
3. Edit the `.env` file with your Groq API key if needed

### Option 2: Manual Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Groq API key in `.env`:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. Start the server:
   ```bash
   python mental_health_chatbot.py
   ```

## Getting Your Groq API Key

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## How It Works

### Frontend Integration
- The chatbot appears as a **floating chat icon** in the bottom-right corner of the student dashboard
- Click the icon to open/close the chat window
- Fully integrated with your React application using TypeScript

### Backend API
- **Endpoint**: `http://localhost:8000/chat/`
- **Method**: POST
- **Payload**: 
  ```json
  {
    "message": "User's message",
    "conversation_id": "unique_conversation_id"
  }
  ```

### Mental Health Context
The AI assistant is specifically trained to:
- Provide empathetic emotional support
- Share evidence-based coping strategies
- Recognize and respond to crisis situations
- Guide students to appropriate resources
- Maintain professional boundaries

### Crisis Safety Features
- Detects crisis keywords automatically
- Provides immediate crisis resources (988, Crisis Text Line)
- Encourages professional help when needed
- Never replaces professional mental health care

## API Endpoints

- `GET /` - Welcome message and API info
- `POST /chat/` - Main chat endpoint
- `GET /health` - Health check endpoint

## Conversation Management

- Each chat session has a unique conversation ID
- Conversations maintain context throughout the session
- System prompt includes mental health expertise and crisis protocols
- Sessions are temporary and not permanently stored

## Troubleshooting

### Common Issues:

1. **"Unable to connect to chatbot service"**
   - Make sure the backend server is running on port 8000
   - Check that your Groq API key is set correctly in `.env`

2. **Import errors in React**
   - Make sure `FloatingChatbot.tsx` is in your components directory
   - Check that the import path is correct in your dashboard

3. **API key errors**
   - Verify your Groq API key is valid and not expired
   - Make sure the `.env` file is in the backend directory

### Testing the Backend

You can test the API directly:

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I am feeling stressed about exams", "conversation_id": "test_123"}'
```

## Files Structure

```
backend/
├── mental_health_chatbot.py  # Main FastAPI server
├── requirements.txt          # Python dependencies
├── setup_and_run.bat        # Automated setup script
├── .env                     # API keys (keep private!)
└── README.md               # This file
```

## Integration Points

The chatbot is integrated into:
- `src/components/FloatingChatbot.tsx` - Main chat component
- `src/services/chatbotService.ts` - API communication service  
- `src/pages/dashboard/StudentDashboard.tsx` - Displays the chat widget

## Support

If you encounter any issues:
1. Check the console for error messages
2. Verify the backend server is running
3. Ensure your API key is valid
4. Check network connectivity between frontend and backend

---

**Important**: This chatbot is designed to support students but should never replace professional mental health care. Always encourage users to seek appropriate professional help when needed.