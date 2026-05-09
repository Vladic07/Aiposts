# AI Content Studio

AI Content Studio is a self-hosted AI-powered content assistant for social media.

It helps manage content profiles, text styles, image styles, generated posts, generation history, tags, statuses, and AI model settings. The current implementation is the first vertical MVP slice from `ai_content_studio_mvp_tz.md`.

## What Works Now

- FastAPI backend on `http://localhost:8000`
- API docs on `http://localhost:8000/docs`
- Next.js frontend on `http://localhost:3000`
- SQLite persistence
- Default local user without registration
- CRUD for content profiles, text styles, image styles, posts, generation sessions, and settings
- Post generation endpoint with OpenAI Responses API when `OPENAI_API_KEY` is set
- Deterministic local fallback generation when no API key is set
- Docker Compose files for local/server launch

## Environment

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` to enable real AI generation. Without it, the backend returns structured fallback content so the app remains usable. The default text model is controlled by Settings and can also be overridden with `DEFAULT_TEXT_MODEL`.

## Run With Docker Compose

```bash
docker compose up --build
```

Open:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Backend docs: `http://localhost:8000/docs`

## Run Locally Without Docker

Backend:

```bash
python -m pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Verification

Backend tests:

```bash
python -m pytest backend/tests -q
```

Frontend lint and build:

```bash
cd frontend
npm run lint
npm run build
```

## MVP Boundary

This slice does not include authentication, billing, social network publishing, Telegram bot, real image generation, team mode, marketplace, or calendar. Image generation is represented by structured `image_prompt` output, matching the cheaper first MVP mode in the brief.
