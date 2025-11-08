from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.models import StudyPlan, UploadedFile, Topic
from app.services.llm_service import LLMService
from typing import Dict, List
import json

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])
llm_service = LLMService()

# In-memory conversation storage (use Redis in production)
conversation_histories: Dict[str, List[Dict]] = {}

@router.post("/ask")
async def ask_question(
    question: str,
    plan_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Ask chatbot a question about study materials
    Context-aware responses using PDF content
    """
    try:
        print(f"\n{'='*60}")
        print(f"💬 Chatbot Question")
        print(f"   User: {user_id}, Plan: {plan_id}")
        print(f"   Question: {question}")
        print(f"{'='*60}")
        
        # Get study plan
        study_plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
        if not study_plan:
            raise HTTPException(status_code=404, detail="Study plan not found")
        
        # Get uploaded files for context
        uploaded_files = db.query(UploadedFile).filter(
            UploadedFile.plan_id == plan_id
        ).all()
        
        context_text = ""
        for file in uploaded_files[:3]:  # Limit to 3 files
            if file.extracted_text:
                context_text += f"\n--- {file.filename} ---\n"
                context_text += file.extracted_text[:2000]  # First 2000 chars
        
        # Get topics
        topics = db.query(Topic).filter(Topic.plan_id == plan_id).all()
        topics_list = ", ".join([t.name for t in topics])
        
        # Get conversation history
        conversation_key = f"{user_id}_{plan_id}"
        history = conversation_histories.get(conversation_key, [])
        
        # Build system prompt
        system_prompt = f"""You are an AI study assistant helping a student prepare for their {study_plan.exam_type} exam in {study_plan.subject}.

**Study Materials Context:**
{context_text}

**Topics Covered:**
{topics_list}

**Your Role:**
- Answer questions clearly and concisely (under 150 words)
- Relate answers to the study materials when relevant
- Provide examples and explanations
- Be encouraging and supportive
- If asked about something not in the materials, give general knowledge but mention it's not in their study plan

**Response Style:**
- Use bullet points for lists
- Be conversational and friendly
- End with "Any other questions?" when appropriate"""

        # Add conversation history
        history_text = ""
        if history:
            history_text = "\n\n**Previous conversation:**\n"
            for msg in history[-5:]:  # Last 5 messages
                history_text += f"Student: {msg['question']}\nYou: {msg['answer']}\n\n"
        
        full_prompt = f"{history_text}\n**Student's question:** {question}\n\n**Your answer:**"
        
        # Call LLM with Groq (fast and free for chatbot)
        result = llm_service.generate_content(
            prompt=full_prompt,
            system_instruction=system_prompt,
            temperature=0.7,
            max_tokens=500,
            preferred_provider='groq'  # Groq for chatbot
        )
        
        if not result['success']:
            raise Exception(result['error'])
        
        answer = result['text'].strip()
        
        # Store in conversation history
        if conversation_key not in conversation_histories:
            conversation_histories[conversation_key] = []
        
        conversation_histories[conversation_key].append({
            "question": question,
            "answer": answer,
            "provider": result['provider']
        })
        
        # Limit history to last 20 messages
        if len(conversation_histories[conversation_key]) > 20:
            conversation_histories[conversation_key] = conversation_histories[conversation_key][-20:]
        
        print(f"✓ Answer generated ({len(answer)} chars)")
        print(f"   Provider: {result['provider']}")
        
        return {
            "question": question,
            "answer": answer,
            "provider_used": result['provider'],
            "has_context": len(context_text) > 0,
            "conversation_length": len(conversation_histories.get(conversation_key, []))
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}/{plan_id}")
async def get_conversation_history(
    user_id: int,
    plan_id: int
):
    """Get conversation history"""
    conversation_key = f"{user_id}_{plan_id}"
    history = conversation_histories.get(conversation_key, [])
    
    return {
        "conversation_id": conversation_key,
        "message_count": len(history),
        "messages": history
    }

@router.delete("/history/{user_id}/{plan_id}")
async def clear_conversation_history(
    user_id: int,
    plan_id: int
):
    """Clear conversation history"""
    conversation_key = f"{user_id}_{plan_id}"
    if conversation_key in conversation_histories:
        del conversation_histories[conversation_key]
    
    return {"message": "Conversation history cleared"}

@router.get("/quick-help")
async def get_quick_help(
    topic: str,
    help_type: str  # "explain", "example", "tips", "mistakes"
):
    """Quick help prompts"""
    
    prompts = {
        "explain": f"Explain {topic} in simple terms with an example (max 100 words).",
        "example": f"Give a practical example of {topic} with step-by-step solution.",
        "tips": f"Give 3 study tips and memory tricks for {topic}.",
        "mistakes": f"What are common mistakes students make with {topic}?"
    }
    
    question = prompts.get(help_type, f"Tell me about {topic}")
    
    result = llm_service.generate_content(
        prompt=question,
        temperature=0.7,
        max_tokens=300,
        preferred_provider='groq'
    )
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return {
        "topic": topic,
        "help_type": help_type,
        "answer": result['text'],
        "provider": result['provider']
    }

@router.get("/providers")
async def get_available_providers():
    """Get list of available LLM providers"""
    return {
        "available": llm_service.get_available_providers(),
        "default": llm_service.default_provider,
        "order": llm_service.provider_order
    }
