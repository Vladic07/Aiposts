from __future__ import annotations

import os

from openai import OpenAI
from pydantic import ValidationError

from app.models import ContentProfile, ImageStyle, TextStyle
from app.prompt_builder import build_generation_prompt
from app.schemas import GeneratePostRequest, GeneratedResult


def fallback_generation(
    request: GeneratePostRequest,
    profile: ContentProfile,
    text_style: TextStyle | None,
    image_style: ImageStyle | None,
) -> GeneratedResult:
    tone = profile.tone or (text_style.description if text_style else None) or "clear and specific"
    platform_text = {}
    for platform in request.platforms:
        platform_text[platform] = {
            "post": (
                f"{request.topic}\n\n"
                f"Angle: make this useful for {profile.audience or 'the target audience'}.\n"
                f"Tone: {tone}.\n"
                f"CTA: {request.goal or 'Save this idea and reuse it when it fits.'}"
            ),
            "cta": request.goal or "Save this for later.",
            "format_notes": f"Adapted for {platform}.",
        }

    image_prompt = (
        f"Create a realistic, specific visual for '{request.topic}' in the context of "
        f"{profile.name}. {image_style.prompt_addon if image_style else 'Natural light, clean composition.'}"
    )

    return GeneratedResult(
        instagram=platform_text.get("instagram", {}),
        facebook=platform_text.get("facebook", {}),
        x=platform_text.get("x", platform_text.get("twitter", {})),
        linkedin=platform_text.get("linkedin", {}),
        stories=[
            {"screen": 1, "text": request.topic, "visual_idea": "Show the concrete situation."},
            {"screen": 2, "text": request.goal or "Why it matters", "visual_idea": "Show the benefit."},
            {"screen": 3, "text": "Simple next step", "visual_idea": "Show the action."},
        ],
        reels={
            "idea": f"A short practical clip about {request.topic}.",
            "script": "Hook, concrete example, one takeaway, soft CTA.",
            "shot_list": ["Opening detail", "Main example", "Result or takeaway"],
        },
        image_prompt={"prompt": image_prompt, "negative_prompt": "generic stock photo, clutter", "text_on_image": ""},
        hooks=[
            {"text": f"Most posts about {request.topic} miss the practical part.", "why_it_can_work": "Creates tension."},
            {"text": f"Here is a simpler way to think about {request.topic}.", "why_it_can_work": "Promises clarity."},
        ],
        analysis={
            "hook_score": 7,
            "clarity_score": 8,
            "originality_score": 6,
            "platform_fit_score": 7,
            "viral_potential_score": 5,
            "strengths": ["Specific topic", "Clear CTA", "Reusable platform structure"],
            "weaknesses": ["Fallback output is not model-generated"],
            "improvement_suggestions": ["Add a concrete personal example", "Tighten the first line per platform"],
            "risk_flags": [],
        },
    )


def generate_post_content(
    request: GeneratePostRequest,
    profile: ContentProfile,
    text_style: TextStyle | None,
    image_style: ImageStyle | None,
) -> tuple[GeneratedResult, str]:
    model = request.model or os.getenv("DEFAULT_TEXT_MODEL", "gpt-4.1-mini")
    if not os.getenv("OPENAI_API_KEY"):
        return fallback_generation(request, profile, text_style, image_style), "fallback-local"

    client = OpenAI()
    prompt = build_generation_prompt(request, profile, text_style, image_style)
    try:
        response = client.responses.parse(
            model=model,
            input=prompt,
            text_format=GeneratedResult,
        )
        parsed = response.output_parsed
        if parsed:
            return parsed, model
        return GeneratedResult.model_validate_json(response.output_text), model
    except (ValidationError, Exception):
        return fallback_generation(request, profile, text_style, image_style), "fallback-local"
