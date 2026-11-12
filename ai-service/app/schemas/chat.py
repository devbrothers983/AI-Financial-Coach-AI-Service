from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):

    role: Literal["user", "assistant"]

    content: str = Field(max_length=6000)


class ChatRequest(BaseModel):

    message: str = Field(min_length=1, max_length=1000)

    history: List[ChatMessage] = Field(default=[], max_length=20)

    # Figures already calculated by the backend
    financial_context: Dict[str, Any]


class ChatResponse(BaseModel):

    reply: str
