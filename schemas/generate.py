from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt to send to the model")
    model: Optional[str] = Field(None, description="OpenAI model id to use")
    temperature: Optional[float] = Field(
        None, ge=0.0, le=2.0, description="Sampling temperature"
    )
    max_tokens: Optional[int] = Field(
        None, ge=1, le=4000, description="Maximum tokens to generate"
    )


class GenerateResponse(BaseModel):
    text: str
    model: str
