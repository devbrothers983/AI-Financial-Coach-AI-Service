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

    user_context = f"""
Purchase:

Name: {financial_data.purchase_name}
Price: ${financial_data.purchase_price}
Reason: {financial_data.reason}


Financial Situation:

Monthly Income:
${financial_data.monthly_income}

Monthly Expenses:
${financial_data.monthly_expenses}

Net Cash Flow:
${financial_data.net_cash_flow}

Total Budget:
${financial_data.total_budget}

Budget Remaining:
${financial_data.budget_remaining}

Savings Rate:
{financial_data.savings_rate}%


Savings Goals:

{
    json.dumps(
        [
            goal.model_dump()
            for goal in financial_data.goals
        ],
        indent=2
    )
}


Analyze whether this purchase is financially reasonable.

Return:

- recommendation
- explanation
- risk_level
- suggested_action
"""


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


    return result 
