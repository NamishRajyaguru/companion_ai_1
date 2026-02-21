from fastapi import APIRouter
from pydantic import BaseModel
from app.session_manager import load_session, save_session
from app.services.chat_engine import generate_reply, bootstrap_messages

router = APIRouter()

class ChatInput(BaseModel):
    message: str


from app.services.chat_engine import generate_reply, bootstrap_messages

@router.post("/chat")
def chat(input: ChatInput):
    messages = load_session()

    if not messages:
        messages = bootstrap_messages()

    reply = generate_reply(input.message, messages)

    save_session(messages)
    return {"reply": reply}

@router.get("/history")
def get_history():
    messages = load_session()
    return {
        "messages": [
            m for m in messages
            if m["role"] in ("user", "assistant")
        ]
    }
