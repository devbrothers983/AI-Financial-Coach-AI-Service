import hmac
import os

from fastapi import Header, HTTPException  # type: ignore[reportMissingImports]


# ========================================
# Only the Backend May Use This Service
# ========================================
# Every request here spends the Groq account's quota, so the backend proves
# itself with a shared key. The check turns on once AI_SERVICE_KEY is set,
# so the service keeps working while the key is being added to both services.

def require_internal_key(
    x_internal_key: str | None = Header(default=None),
) -> None:

    expected = os.getenv("AI_SERVICE_KEY")

    if not expected:
        return

    if not x_internal_key or not hmac.compare_digest(x_internal_key, expected):
        raise HTTPException(status_code=401, detail="Unauthorized")
