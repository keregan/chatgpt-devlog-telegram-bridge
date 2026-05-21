from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from app.config import BRIDGE_SECRET_TOKEN
from app.telegram_sender import send_telegram_message


app = FastAPI(
    title="ChatGPT DevLog Telegram Bridge",
    description="Service for publishing project progress posts from ChatGPT to Telegram",
    version="1.0.0"
)


class DevLogPost(BaseModel):
    text: str


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "ChatGPT DevLog Telegram Bridge"
    }


@app.post("/publish-devlog")
def publish_devlog(
    post: DevLogPost,
    x_bridge_token: str = Header(default="", alias="x-bridge-token")
):
    expected_token = (BRIDGE_SECRET_TOKEN or "").strip()
    received_token = (x_bridge_token or "").strip()

    if not expected_token:
        raise HTTPException(
            status_code=500,
            detail="Bridge secret token is not configured"
        )

    if received_token != expected_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid bridge token"
        )

    telegram_result = send_telegram_message(post.text)

    return {
        "status": "ok",
        "post_preview": post.text,
        "telegram": telegram_result
    }