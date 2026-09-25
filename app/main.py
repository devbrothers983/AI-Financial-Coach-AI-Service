from fastapi import FastAPI  # type: ignore[reportMissingImports]

from app.schemas.affordability import (
    AffordabilityRequest,
    AffordabilityResponse,
)

from app.services.affordability_service import (
    analyze_affordability,
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
)
def affordability(
    request: AffordabilityRequest
):

    return analyze_affordability(request)