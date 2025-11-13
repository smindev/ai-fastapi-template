import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIService:
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set. Add it to your .env")
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL"),
            organization=os.getenv("OPENAI_ORG"),
        )

    def generate_text(
        self,
        prompt: str,
        model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        resp = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""
