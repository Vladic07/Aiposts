from types import SimpleNamespace

from app.prompt_builder import build_generation_prompt
from app.schemas import GeneratePostRequest


def test_generation_prompt_is_structured_as_system_and_user_messages() -> None:
    request = GeneratePostRequest(
        profile_id=1,
        topic="Launch a local AI workshop",
        goal="Get qualified signups",
        platforms=["x", "linkedin"],
        format="post",
        length="short",
        language="en",
    )
    profile = SimpleNamespace(
        name="AI Builder",
        profile_type="expert",
        audience="technical founders",
        positioning="practical AI operator",
        tone="direct and concrete",
        forbidden_words="revolutionary",
        avoid_topics="generic hype",
        content_pillars=["workflows", "case studies"],
        favorite_words="specific, useful",
        additional_notes="Prefer real examples.",
    )
    text_style = SimpleNamespace(
        rules="Short sentences. No filler.",
        examples=["A useful post starts with a specific problem."],
        emoji_level="none",
        post_length="short",
        cta_style="direct",
    )
    image_style = SimpleNamespace(
        prompt_addon="Clean workspace, natural light.",
        colors=["black", "white"],
        mood="focused",
        composition="wide shot",
        avoid="stock photo look",
    )

    messages = build_generation_prompt(request, profile, text_style, image_style)

    assert [message["role"] for message in messages] == ["system", "user"]
    assert "Return only structured content that matches the provided schema" in messages[0]["content"]
    assert "Audience: technical founders" in messages[1]["content"]
    assert "Platforms: x, linkedin" in messages[1]["content"]
    assert "Text style examples" in messages[1]["content"]
    assert "Clean workspace, natural light." in messages[1]["content"]
