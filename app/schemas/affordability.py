from typing import List, Literal

from pydantic import BaseModel, Field


class GoalContext(BaseModel):

    title: str

    target_amount: float

    current_amount: float = 0

    remaining_amount: float

    priority: str

    target_date: str | None = None


class AffordabilityRequest(BaseModel):

    purchase_name: str = Field(min_length=1, max_length=100)

    purchase_price: float = Field(gt=0)

    reason: str | None = Field(default=None, max_length=300)

    currency: str = "USD"

    # This month so far
    monthly_income: float

    monthly_expenses: float

    net_cash_flow: float

    savings_rate: float | None = None

    days_left_in_month: int | None = None

    # This month's budget, before and after buying
    total_budget: float | None = None

    budget_remaining: float | None = None

    budget_after_purchase: float | None = None

    daily_allowance_before: float | None = None

    daily_allowance_after: float | None = None

    # Average of recent complete months
    typical_monthly_income: float | None = None

    typical_monthly_savings: float | None = None

    goal_delay_weeks: float | None = None

    # The backend's rule: the answer may be more cautious than this, never less
    minimum_recommendation: Literal["AFFORDABLE", "CAUTION", "NOT_RECOMMENDED"] = "AFFORDABLE"

    goals: List[GoalContext] = Field(default=[], max_length=50)


class AffordabilityResponse(BaseModel):

    recommendation: Literal["AFFORDABLE", "CAUTION", "NOT_RECOMMENDED"]

    explanation: str

    risk_level: Literal["LOW", "MEDIUM", "HIGH"]

    suggested_action: str
