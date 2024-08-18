from supabase import Client

async def save_chat_log(supabase: Client, user_message: str, assistant_response: str):
    try:
        data = supabase.table('chat_logs').insert({
            "user_message": user_message,
            "assistant_response": assistant_response
        }).execute()
        return data
    except Exception as e:
        print(f"Error saving chat log: {e}")
        return None