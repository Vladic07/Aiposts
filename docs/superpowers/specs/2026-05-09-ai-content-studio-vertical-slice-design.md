# AI Content Studio Vertical Slice Design

## Scope

Build the first runnable slice of AI Content Studio from the existing MVP brief. The slice must start with `docker compose up`, expose a FastAPI backend on port `8000`, expose a Next.js frontend on port `3000`, persist data in SQLite, and provide working CRUD for the main memory objects.

This slice includes:

- Local single-user mode with a default user created on startup.
- Content profiles, text styles, image styles, posts, generation sessions, and AI settings.
- Auto post generation endpoint backed by OpenAI Responses API when `OPENAI_API_KEY` is present.
- Deterministic local fallback generation when no API key is configured.
- Basic responsive frontend screens for Dashboard, Profiles, Text Styles, Image Styles, Generate, History, and Settings.

This slice does not include:

- Authentication, billing, teams, publishing integrations, Telegram bot, real image generation, marketplace, or calendar.
- Full guided multi-step UX. The backend stores sessions now; the guided workflow can be layered on top after the core slice is stable.

## Architecture

Backend uses FastAPI with router modules per domain. SQLAlchemy 2.0 typed ORM models define the database. Pydantic v2 schemas validate requests and responses. A request-scoped database `Session` is injected through a FastAPI dependency.

Frontend uses Next.js App Router with client-side API calls to the backend. The UI is intentionally dense and utility-focused: sidebar navigation, compact forms, and direct management screens rather than a marketing page.

AI generation is isolated behind `ai_service.py` and `prompt_builder.py`. The rest of the app only depends on a structured generation result, so model/API changes remain localized.

## Data Model

The database contains:

- `users`: one default local user.
- `content_profiles`: profile memory and platform strategy fields.
- `text_styles`: reusable voice rules.
- `image_styles`: reusable image prompt preferences.
- `posts`: generated output, analysis, tags, status, and source metadata.
- `generation_sessions`: guided-mode state and intermediate artifacts.
- `settings`: provider/model/default language settings.

Flexible fields such as platforms, content pillars, generated content, score, and analysis are stored as JSON to preserve MVP velocity while keeping SQL rows queryable.

## API

Endpoints follow the brief:

- `/api/content-profiles`
- `/api/text-styles`
- `/api/image-styles`
- `/api/posts`
- `/api/posts/generate`
- `/api/generation-sessions`
- `/api/settings`
- `/api/health`

`/api/content-profiles/analyze-description`, `/api/content-profiles/improve`, and `/api/text-styles/analyze-examples` return structured AI-assisted drafts using the same AI abstraction.

## Testing

Backend tests cover startup defaults, CRUD behavior, post status updates, and deterministic generation without an API key. Frontend verification uses `npm run lint` and `npm run build`.

## Documentation

README documents local Python/npm development, Docker Compose launch, environment variables, and the current MVP boundary.
