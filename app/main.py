from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from app.config import BRIDGE_SECRET_TOKEN
from app.telegram_sender import send_telegram_message


app = FastAPI(
    title="ChatGPT DevLog Telegram Bridge",
    description="Service for publishing project progress posts from ChatGPT to Telegram",
    version="1.3.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "chatgpt-devlog-telegram-bridge"
    }

class DevLogPost(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)


def validate_bridge_token(x_bridge_token: str) -> None:
    expected_token = (BRIDGE_SECRET_TOKEN or "").strip()
    received_token = (x_bridge_token or "").strip()

    if not expected_token:
        raise HTTPException(
            status_code=500,
            detail="Bridge secret token is not configured",
        )

    if received_token != expected_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid bridge token",
        )


def format_devlog_post(post: DevLogPost) -> str:
    tags = []

    for tag in post.tags:
        clean_tag = tag.strip().replace(" ", "_").replace("#", "")
        if clean_tag:
            tags.append(f"#{clean_tag}")

    tags_block = ""

    if tags:
        tags_block = "\n\n" + " ".join(tags)

    return f"🚀 {post.title}\n\n{post.content}{tags_block}"


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "ChatGPT DevLog Telegram Bridge",
    }


@app.post("/preview-devlog")
def preview_devlog(
    post: DevLogPost,
    x_bridge_token: str = Header(default="", alias="x-bridge-token"),
):
    validate_bridge_token(x_bridge_token)

    formatted_text = format_devlog_post(post)

    return {
        "status": "ok",
        "post_preview": formatted_text,
    }


@app.post("/publish-devlog")
def publish_devlog(
    post: DevLogPost,
    x_bridge_token: str = Header(default="", alias="x-bridge-token"),
):
    validate_bridge_token(x_bridge_token)

    formatted_text = format_devlog_post(post)
    telegram_result = send_telegram_message(formatted_text)

    if not telegram_result.get("ok"):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Telegram message was not delivered",
                "telegram": telegram_result,
            },
        )

    return {
        "status": "ok",
        "post_preview": formatted_text,
        "telegram": telegram_result,
    }
