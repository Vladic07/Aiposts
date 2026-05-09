from app.models import ContentProfile, ImageStyle, TextStyle
from app.schemas import GeneratePostRequest

PromptMessage = dict[str, str]


def format_list(values: list[str] | None) -> str:
    return ", ".join(values or []) or "not specified"


def optional_text(instance: object, field: str) -> str:
    value = getattr(instance, field, None)
    return value or "not specified"


def build_generation_prompt(
    request: GeneratePostRequest,
    profile: ContentProfile,
    text_style: TextStyle | None,
    image_style: ImageStyle | None,
) -> list[PromptMessage]:
    style_rules = text_style.rules if text_style else "Use the profile tone and avoid generic filler."
    style_examples = "\n".join(f"- {example}" for example in (text_style.examples if text_style else [])) or "- not specified"
    visual_rules = image_style.prompt_addon if image_style else "Create a concrete visual prompt."
    system_message = """
You are a professional social media content assistant for a local content studio.
Return only structured content that matches the provided schema. Write complete,
ready-to-use posts. Avoid generic filler, vague claims, and invented facts.
""".strip()
    user_message = f"""
Content profile
- Name: {profile.name}
- Type: {optional_text(profile, "profile_type")}
- Audience: {optional_text(profile, "audience")}
- Positioning: {optional_text(profile, "positioning")}
- Tone: {optional_text(profile, "tone")}
- Forbidden words: {optional_text(profile, "forbidden_words")}
- Avoid topics: {optional_text(profile, "avoid_topics")}
- Content pillars: {format_list(getattr(profile, "content_pillars", []))}
- Favorite words: {optional_text(profile, "favorite_words")}
- Additional notes: {optional_text(profile, "additional_notes")}

Text style rules
{style_rules}
- Emoji level: {text_style.emoji_level if text_style else "low"}
- Post length: {text_style.post_length if text_style else request.length}
- CTA style: {text_style.cta_style if text_style else "soft"}

Text style examples
{style_examples}

Image style rules
{visual_rules}
- Colors: {format_list(image_style.colors if image_style else [])}
- Mood: {image_style.mood if image_style else "not specified"}
- Composition: {image_style.composition if image_style else "not specified"}
- Avoid: {image_style.avoid if image_style else "not specified"}

User task
- Topic: {request.topic}
- Goal: {request.goal or "not specified"}
- Platforms: {", ".join(request.platforms)}
- Format: {request.format}
- Length: {request.length}
- Language: {request.language}
- Variants: {request.variants}

Output requirements
- Fill platform-specific objects only for requested platforms when possible.
- Include hooks with practical reasoning.
- Include a concrete image_prompt with negative_prompt.
- Score analysis from 0 to 10 and include strengths, weaknesses, suggestions, and risk flags.
""".strip()
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
