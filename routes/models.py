from fastapi import APIRouter, Depends, HTTPException

from services.ai_service import AIService

router = APIRouter(tags=["ai"])


def get_ai_service() -> AIService:
    return AIService()


@router.get("/models", summary="List available OpenAI models")
async def list_models(svc: AIService = Depends(get_ai_service)):
    try:
        # Using OpenAI Python SDK v1
        models = svc.client.models.list()
        # Extract IDs and sort for stable output
        ids = sorted([m.id for m in models.data])
        return {"models": ids}
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"Failed to list models: {e}")


__all__ = ["router", "get_ai_service"]
