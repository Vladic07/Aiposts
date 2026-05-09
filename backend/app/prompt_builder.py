from app.models import ContentProfile, ImageStyle, TextStyle
from app.schemas import GeneratePostRequest


def build_generation_prompt(
    request: GeneratePostRequest,
    profile: ContentProfile,
    text_style: TextStyle | None,
    image_style: ImageStyle | None,
) -> str:
    style_rules = text_style.rules if text_style else "Use the profile tone and avoid generic filler."
    visual_rules = image_style.prompt_addon if image_style else "Create a concrete visual prompt."
    return f"""
You are a professional social media content assistant.

Content profile:
- Name: {profile.name}
- Type: {profile.profile_type or "not specified"}
- Audience: {profile.audience or "not specified"}
- Positioning: {profile.positioning or "not specified"}
- Tone: {profile.tone or "not specified"}
- Forbidden words: {profile.forbidden_words or "not specified"}
- Avoid topics: {profile.avoid_topics or "not specified"}

Text style rules:
{style_rules}

Image style rules:
{visual_rules}

User task:
- Topic: {request.topic}
- Goal: {request.goal or "not specified"}
- Platforms: {", ".join(request.platforms)}
- Format: {request.format}
- Length: {request.length}
- Language: {request.language}

Return structured JSON with platform-specific posts, stories, reels idea, hooks,
image_prompt, and analysis scores from 0 to 10.
""".strip()
