from app.main import DevLogPost, format_devlog_post


def test_format_devlog_post_with_tags():
    post = DevLogPost(
        title="Deployment complete",
        content="Project was deployed with Docker, Caddy and HTTPS.",
        tags=["DevOps", "Docker", "FastAPI"],
    )

    result = format_devlog_post(post)

    assert result == (
        "🚀 Deployment complete\n\n"
        "Project was deployed with Docker, Caddy and HTTPS.\n\n"
        "#DevOps #Docker #FastAPI"
    )


def test_format_devlog_post_without_tags():
    post = DevLogPost(
        title="Simple update",
        content="Added a new API endpoint.",
        tags=[],
    )

    result = format_devlog_post(post)

    assert result == (
        "🚀 Simple update\n\n"
        "Added a new API endpoint."
    )


def test_format_devlog_post_cleans_tags():
    post = DevLogPost(
        title="Tag cleanup",
        content="Tags should be formatted correctly.",
        tags=["#DevOps", "Fast API", "  Docker  "],
    )

    result = format_devlog_post(post)

    assert "#DevOps" in result
    assert "#Fast_API" in result
    assert "#Docker" in result
