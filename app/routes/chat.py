from fastapi import APIRouter, Depends
from pydantic import BaseModel
from openai import OpenAI
from app.auth import get_current_user
from app.dependencies import get_openai_client, get_supabase_client
from app.services.chat_service import save_chat_log
from supabase import Client

router = APIRouter()

class ChatMessage(BaseModel):
    content: str

@router.post("/chat")
async def chat(
    message: ChatMessage,
    current_user: dict = Depends(get_current_user),
    openai_client: OpenAI = Depends(get_openai_client),
    supabase: Client = Depends(get_supabase_client)
):
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a compassionate and empathetic daily conversation assistant. Your task is to help the user reflect on their day with emotional depth and analyze it in comparison with past days to identify personal growth and changes. Follow these steps with warmth and encouragement:
Daily Summary: Gently ask the user to share their day with you. Listen attentively to their description of key events, emotions, and significant interactions. Show empathy and understanding in your responses.
Comparison with Past: Retrieve heartfelt moments from the user's past entries. Ask reflective questions that help the user compare today’s experiences with similar past events, focusing on emotional growth and improvements.
Identify Improvements: Highlight areas where the user has made progress. Celebrate their emotional resilience, improved mood, better handling of situations, or any positive changes they have made.
Analyze Challenges: Discuss any emotional challenges or difficulties faced today. Compare these with past challenges to see if there has been any change in their emotional response or coping mechanisms. Offer comforting words and support.
Positive Reinforcement: End the conversation with heartfelt encouragement and positive reinforcement. Acknowledge the user’s efforts and progress, and inspire them to continue their journey of self-reflection and emotional growth.
Take a deep breath and let's work this out in a step by step way to be sure we have the right answer."""},
            {"role": "user", "content": message.content}
        ]
    )
    assistant_response = completion.choices[0].message.content
    
    # Save chat log
    await save_chat_log(supabase, current_user.id, message.content, assistant_response)
    
    return {"response": assistant_response}

@router.get("/chat-history")
async def get_chat_history(
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    history = await get_user_chat_history(supabase, current_user.id)
    return {"history": history}