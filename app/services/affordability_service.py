import json
import os

from dotenv import load_dotenv
from groq import Groq

from app.schemas.affordability import (
    AffordabilityRequest,
    AffordabilityResponse,
)

from app.prompts.affordability_prompt import (
    AFFORDABILITY_SYSTEM_PROMPT,
)


load_dotenv()


# ========================================
# Create Groq Client
# ========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ========================================
# Analyze Affordability
# ========================================

def analyze_affordability(
    financial_data: AffordabilityRequest
) -> AffordabilityResponse:


    # ========================================
    # Create User Context
    # ========================================
    # Sent as JSON so every figure reaches the AI exactly, nulls included.

    user_context = (
        "Should I buy this? Here is the purchase and my financial data:\n\n"
        + json.dumps(financial_data.model_dump(), indent=2)
    )


    # ========================================
    # Call Groq
    # ========================================

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[

            {
                "role": "system",
                "content":
                    AFFORDABILITY_SYSTEM_PROMPT,
            },

            {
                "role": "user",
                "content":
                    user_context,
            },

        ],


        # ========================================
        # Structured JSON Output
        # ========================================

        response_format={

            "type": "json_schema",

            "json_schema": {

                "name":
                    "affordability_response",

                "strict":
                    True,

                "schema": {

                    "type":
                        "object",

                    "properties": {

                        "recommendation": {
                            "type": "string",
                            "enum": [
                                "AFFORDABLE",
                                "CAUTION",
                                "NOT_RECOMMENDED",
                            ],
                        },

                        "explanation": {
                            "type": "string",
                        },

                        "risk_level": {
                            "type": "string",
                            "enum": [
                                "LOW",
                                "MEDIUM",
                                "HIGH",
                            ],
                        },

                        "suggested_action": {
                            "type": "string",
                        },

                    },

                    "required": [
                        "recommendation",
                        "explanation",
                        "risk_level",
                        "suggested_action",
                    ],

                    "additionalProperties":
                        False,
                },
            },
        },
    )


    # ========================================
    # Get JSON String From Groq
    # ========================================

    content = response.choices[0].message.content


    # ========================================
    # Validate With Pydantic
    # ========================================

    result = (
        AffordabilityResponse
        .model_validate_json(content)
    )


    # ========================================
    # Never Softer Than the Backend's Rule
    # ========================================

    order = ["AFFORDABLE", "CAUTION", "NOT_RECOMMENDED"]
    risk_for = {"AFFORDABLE": "LOW", "CAUTION": "MEDIUM", "NOT_RECOMMENDED": "HIGH"}

    if order.index(result.recommendation) < order.index(financial_data.minimum_recommendation):
        result.recommendation = financial_data.minimum_recommendation
        result.risk_level = risk_for[result.recommendation]


    return result
