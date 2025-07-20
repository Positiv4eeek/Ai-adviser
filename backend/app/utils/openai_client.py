from openai import OpenAI
from app.db import settings
from sqlalchemy.orm import Session
from app.models import AIPrompt
from fastapi import HTTPException

client = OpenAI(api_key=settings.openai_api_key)

def ask_gpt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano", 
            messages=[
                {"role": "system", "content": "You are an academic adviser helping students choose their next courses."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return "Sorry, I couldn't generate a recommendation at this time."
    
def get_prompt_content(name: str, db: Session) -> str:
    prompt = db.query(AIPrompt).filter(AIPrompt.name == name).first()
    if not prompt:
        raise HTTPException(status_code=404, detail=f"Prompt '{name}' not found.")
    return prompt.content