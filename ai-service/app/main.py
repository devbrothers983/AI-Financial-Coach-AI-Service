from fastapi import Depends, FastAPI, HTTPException  # type: ignore[reportMissingImports]

from app.security import require_internal_key

from app.schemas.affordability import (
    AffordabilityRequest,
    AffordabilityResponse,
)

from app.services.affordability_service import (
    analyze_affordability,
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.chat_service import (
    answer_chat,
)


app = FastAPI(
    title="AI Financial Coach Service",
    version="1.0.0",
)


@app.get("/")
def root():

    return {
        "success": True,
        "message": "AI Financial Coach service is running",
    }


@app.post(
    "/ai/affordability",
    response_model=AffordabilityResponse,
    dependencies=[Depends(require_internal_key)],
)
def affordability(
    request: AffordabilityRequest
):

    return analyze_affordability(request)


@app.post(
    "/ai/chat",
    response_model=ChatResponse,
    dependencies=[Depends(require_internal_key)],
)
def chat(
    request: ChatRequest
):

    try:
        return answer_chat(request)
    except Exception as err:
        # the type only: errors can include the user's financial data
        print(f"AI chat failed: {type(err).__name__}")
        raise HTTPException(status_code=502, detail="AI service failed to answer") from None
