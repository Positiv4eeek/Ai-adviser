from openai import OpenAI
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import settings
from app.models import AIPrompt, AISettings

client = OpenAI(api_key=settings.openai_api_key)

def ask_gpt(prompt: str, db: Session) -> str:
    settings_row = db.query(AISettings).first()
    if not settings_row:
        raise HTTPException(status_code=500, detail="AI settings not configured.")

    if not all([settings_row.model, settings_row.system_prompt, settings_row.temperature is not None, settings_row.max_tokens]):
        raise HTTPException(status_code=500, detail="Incomplete AI settings.")

    try:
        response = client.chat.completions.create(
            model=settings_row.model,
            messages=[
                {
                    "role": "system",
                    "content": settings_row.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=settings_row.temperature,
            max_tokens=settings_row.max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return "Извините, не удалось получить ответ от модели."

def get_prompt_content(name: str, db: Session) -> str:
    prompt = db.query(AIPrompt).filter(AIPrompt.name == name).first()
    if not prompt:
        raise HTTPException(status_code=404, detail=f"Prompt '{name}' not found.")
    return prompt.content
