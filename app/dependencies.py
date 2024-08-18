import os
from openai import OpenAI
from supabase import create_client, Client
from fastapi import HTTPException

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found")
    return OpenAI(api_key=api_key)

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)