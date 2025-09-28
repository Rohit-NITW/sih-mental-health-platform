import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("API key for Groq is missing. Please set the GROQ_API_KEY in the .env file.")

app = FastAPI(title="MindWell AI Chatbot", description="Mental health support chatbot for students")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=GROQ_API_KEY)

class UserInput(BaseModel):
    message: str
    role: str = "user"
    conversation_id: str

class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system", 
                "content": """You are MindWell AI, a compassionate and knowledgeable mental health support assistant designed specifically for students. Your role is to:

1. PROVIDE EMOTIONAL SUPPORT: Listen actively and respond with empathy to students' mental health concerns
2. OFFER PRACTICAL GUIDANCE: Share evidence-based coping strategies, stress management techniques, and wellness tips
3. EDUCATE ABOUT MENTAL HEALTH: Provide information about common mental health conditions, symptoms, and when to seek help
4. PROMOTE HELP-SEEKING: Encourage students to reach out to professional support when needed
5. CRISIS AWARENESS: Recognize signs of crisis and provide appropriate resources

IMPORTANT GUIDELINES:
- Always be empathetic, non-judgmental, and supportive
- Never provide medical diagnoses or replace professional mental health care
- If someone expresses thoughts of self-harm or suicide, immediately provide crisis resources
- Focus on student-specific challenges: academic stress, social anxiety, homesickness, financial stress, etc.
- Promote healthy coping strategies and self-care practices
- Encourage connection with campus resources and professional support
- Use a warm, understanding tone while maintaining professional boundaries

CRISIS RESOURCES TO SHARE WHEN NEEDED:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Campus counseling services
- Emergency services: 911

Remember: You are a supportive companion in their mental health journey, not a replacement for professional care."""
            }
        ]
        self.active: bool = True

conversations: Dict[str, Conversation] = {}

def query_groq_api(conversation: Conversation) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation.messages,
            temperature=0.7,  # Slightly lower temperature for more consistent, empathetic responses
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Groq API: {str(e)}")

def get_or_create_conversation(conversation_id: str) -> Conversation:
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    return conversations[conversation_id]

def contains_crisis_keywords(message: str) -> bool:
    """Check if the message contains crisis-related keywords"""
    crisis_keywords = [
        "suicide", "kill myself", "end it all", "don't want to live", 
        "hurt myself", "self harm", "cutting", "overdose", "jump off",
        "hopeless", "no point", "better off dead", "ending my life"
    ]
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in crisis_keywords)

@app.post("/chat/")
async def chat(input: UserInput):
    conversation = get_or_create_conversation(input.conversation_id)

    if not conversation.active:
        raise HTTPException(
            status_code=400, 
            detail="The chat session has ended. Please start a new session."
        )
        
    try:
        # Check for crisis indicators
        if contains_crisis_keywords(input.message):
            # Prepend crisis context to the message
            crisis_context = "\n\n[CRISIS ALERT: The user may be expressing thoughts of self-harm. Respond with immediate crisis resources and supportive language.]"
            input.message += crisis_context
        
        # Append the user's message to the conversation
        conversation.messages.append({
            "role": input.role,
            "content": input.message
        })
        
        response = query_groq_api(conversation)
        
        conversation.messages.append({
            "role": "assistant",
            "content": response
        })
        
        return {
            "response": response,
            "conversation_id": input.conversation_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MindWell AI Chatbot"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to MindWell AI Chatbot API",
        "version": "1.0.0",
        "description": "Mental health support chatbot for students"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)