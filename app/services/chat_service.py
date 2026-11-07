import json
import os

from dotenv import load_dotenv
from groq import Groq

from app.prompts.chat_prompt import CHAT_SYSTEM_PROMPT
from app.schemas.chat import ChatRequest, ChatResponse


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ========================================
# Answer a Question About the User's Money
# ========================================

def answer_chat(request: ChatRequest) -> ChatResponse:

    financial_data = json.dumps(request.financial_context, indent=2)

    messages = [
        {
            "role": "system",
            "content": CHAT_SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": f"The user's financial data:\n\n{financial_data}",
        },
        *[message.model_dump() for message in request.history],
        {
            "role": "user",
            "content": request.message,
        },
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.3,
        max_completion_tokens=1000,
    )

    reply = (response.choices[0].message.content or "").strip()

    if not reply:
        raise ValueError("The AI returned an empty reply")

    return ChatResponse(reply=reply)
