# AI Content Studio Vertical Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable first slice of AI Content Studio with FastAPI, SQLite, Next.js, Docker Compose, CRUD screens, and basic AI-backed post generation.

**Architecture:** FastAPI owns persistence and AI orchestration. Next.js is a separate frontend service that calls the backend API. SQLite stores the MVP data locally, with JSON fields for flexible AI output.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic 2, OpenAI Python SDK, pytest, Next.js 16, React 19, Tailwind CSS 4, Docker Compose.

---

### Task 1: Backend Core

**Files:**
- Create: `backend/app/database.py`
- Create: `backend/app/models.py`
- Create: `backend/app/schemas.py`
- Create: `backend/app/main.py`
- Create: `backend/tests/test_api.py`

- [ ] **Step 1: Write backend API tests**

Create tests for health, default user bootstrap, content profile CRUD, and fallback generation.

- [ ] **Step 2: Run tests and verify they fail**

Run: `python -m pytest backend/tests -q`
Expected: tests fail because app modules do not exist yet.

- [ ] **Step 3: Implement database, models, schemas, app startup, and routers**

Use SQLAlchemy 2 typed models, FastAPI routers, and Pydantic v2 schemas.

- [ ] **Step 4: Run tests and verify they pass**

Run: `python -m pytest backend/tests -q`
Expected: all backend tests pass.

### Task 2: AI Generation Layer

**Files:**
- Create: `backend/app/ai_service.py`
- Create: `backend/app/prompt_builder.py`
- Modify: `backend/app/routers/posts.py`
- Modify: `backend/app/routers/content_profiles.py`
- Modify: `backend/app/routers/text_styles.py`

- [ ] **Step 1: Keep tests deterministic without an API key**

Assert `/api/posts/generate` creates a post with platform variants, hooks, image prompt, and analysis.

- [ ] **Step 2: Implement OpenAI Responses API integration**

Use `OpenAI()` from environment and `responses.parse` for structured output when possible.

- [ ] **Step 3: Keep fallback output structured**

When `OPENAI_API_KEY` is absent, return a deterministic structured result so the app remains usable locally.

### Task 3: Frontend Slice

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/app/layout.tsx`
- Create: `frontend/app/page.tsx`
- Create: `frontend/app/globals.css`
- Create: `frontend/components/AppShell.tsx`
- Create: `frontend/components/ResourceManager.tsx`
- Create: `frontend/components/GeneratePanel.tsx`
- Create: `frontend/lib/api.ts`

- [ ] **Step 1: Build a responsive operational UI**

Create sidebar navigation, dashboard summary, resource CRUD panels, generation form, history list, and settings panel.

- [ ] **Step 2: Connect frontend to backend**

Use `NEXT_PUBLIC_API_URL`, defaulting to `http://localhost:8000`.

- [ ] **Step 3: Verify frontend build**

Run: `npm install` in `frontend`, then `npm run lint` and `npm run build`.

### Task 4: Packaging and Docs

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`
- Create: `docker-compose.yml`
- Create: `.env.example`
- Create: `README.md`

- [ ] **Step 1: Add local and Docker run instructions**

Document env vars, service ports, and verification commands.

- [ ] **Step 2: Verify available commands**

Run backend tests and frontend build locally. Docker verification is skipped if Docker CLI is unavailable.
