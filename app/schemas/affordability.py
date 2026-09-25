from pydantic import BaseModel, Field
from typing import List



class GoalContext(BaseModel):
    title: str
    target_amount: float
    target_amount: float
    remaining_amount: float
    priority: str




class AffordabilityRequest(BaseModel):

    purchase_name: str
    purchase_price: float = Field(
        gt=0
    )

    reason: str | None = None

    monthly_income: float

    monthly_expenses: float

    net_cash_flow: float

    total_budget: float | None = None

    budget_remaining: float | None = None

    savings_rate: float | None = None

    goals: List[GoalContext]  = []



class AffordabilityResponse(BaseModel): 

        recommendation: str

        explanation: str

        risk_level: str

        suggested_action: str