import os

from fastapi import APIRouter, Depends, HTTPException
import anyio
from openai import APIStatusError

from services.ai_service import AIService
from schemas.generate import GenerateRequest, GenerateResponse

router = APIRouter(tags=["ai"])


def get_ai_service() -> AIService:
    return AIService()


@router.post(
    "/generate", response_model=GenerateResponse, summary="Generate text with OpenAI"
)
async def generate(
    req: GenerateRequest, svc: AIService = Depends(get_ai_service)
) -> GenerateResponse:
    try:
        model = req.model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        temperature = req.temperature if req.temperature is not None else 0.7
        max_tokens = req.max_tokens if req.max_tokens is not None else 2000

        text = await anyio.to_thread.run_sync(
            lambda: svc.generate_text(
                prompt=req.prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        )
        return GenerateResponse(text=text, model=model)
    except APIStatusError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=(
                    "OpenAI model not found or not accessible. "
                    "Set OPENAI_MODEL to a model available to your account "
                    "or request access."
                ),
            )
        if e.status_code == 401:
            raise HTTPException(
                status_code=401, detail="Invalid or missing OPENAI_API_KEY"
            )
        if e.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail=(
                    "OpenAI rate limit or quota exceeded. "
                    "Reduce request rate, lower max_tokens, or upgrade quota."
                ),
            )
        raise HTTPException(
            status_code=502, detail=f"OpenAI API error ({e.status_code})"
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate text") from e


__all__ = ["router", "get_ai_service"]
