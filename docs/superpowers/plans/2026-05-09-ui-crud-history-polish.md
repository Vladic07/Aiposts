# UI CRUD History Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the MVP usable as a working local product by adding real UI management for resources, active profile selection, editable History metadata, copy/reuse actions, Settings editing, and missing API regression tests.

**Architecture:** Keep the existing FastAPI resource routers and Next.js single-shell frontend. Backend changes are limited to regression tests unless the tests expose missing behavior. Frontend changes extend the current client-side API layer and components without introducing routing, auth, or a new state library.

**Tech Stack:** FastAPI, SQLAlchemy, pytest, Next.js App Router, React 19, TypeScript, Tailwind CSS, lucide-react.

---

### Task 1: API Regression Coverage

**Files:**
- Modify: `backend/tests/test_api.py`

- [ ] Add tests for text style update/delete, image style update/delete, settings update, generation session create/list/delete, and invalid `profile_id` generation errors.
- [ ] Run `python -m pytest backend/tests -q` and verify the new tests fail if corresponding behavior is missing.
- [ ] Patch backend only if a test exposes a real gap.
- [ ] Run `python -m pytest backend/tests -q` and verify all backend tests pass.

### Task 2: Frontend API Helpers

**Files:**
- Modify: `frontend/lib/api.ts`

- [ ] Add `updateTextStyle`, `deleteTextStyle`, `updateImageStyle`, `deleteImageStyle`, `deleteProfile`, `deletePost`, `listGenerationSessions`, `createGenerationSession`, and `deleteGenerationSession`.
- [ ] Add missing fields used by forms to frontend types, including profile memory fields, post `updated_at`, and settings editable fields.
- [ ] Keep request error handling centralized.

### Task 3: Resource Manager CRUD

**Files:**
- Modify: `frontend/components/ResourceManager.tsx`
- Modify: `frontend/components/AppShell.tsx`

- [ ] Convert resource cards into editable rows with `Edit`, `Save`, `Cancel`, and `Delete`.
- [ ] Reuse the same field metadata for create and edit forms.
- [ ] Wire profiles, text styles, and image styles to their update/delete API calls.
- [ ] Preserve compact operational layout and avoid nested cards.

### Task 4: Active Profile and Generate Reuse

**Files:**
- Modify: `frontend/components/AppShell.tsx`
- Modify: `frontend/components/GeneratePanel.tsx`

- [ ] Track `activeProfileId` in `AppShell`.
- [ ] Let Dashboard and Profiles set the active profile.
- [ ] Preselect active profile in Generate.
- [ ] Support prefilled generation topic/goal/platforms from History reuse actions.

### Task 5: History Workspace

**Files:**
- Modify: `frontend/components/AppShell.tsx`

- [ ] Replace raw History JSON list with a split list/detail workspace.
- [ ] Show full generated fields: content, image prompt, analysis, profile/model/status/tags/notes/date.
- [ ] Add status selector, tags input, notes editor, save metadata action, archive/delete actions.
- [ ] Add copy buttons for generated text and image prompt using `navigator.clipboard`.
- [ ] Add reuse action that opens Generate with the saved topic/profile/platforms.

### Task 6: Settings Form

**Files:**
- Modify: `frontend/components/AppShell.tsx`

- [ ] Replace JSON Settings preview with a form for provider, model names, default language, and daily generation limit.
- [ ] Save through `api.updateSettings`.
- [ ] Refresh local settings state after save.

### Task 7: Verification and Commit

**Files:**
- Read: changed files

- [ ] Re-read changed files for type/import mistakes.
- [ ] Run `python -m pytest backend/tests -q`.
- [ ] Run `npm run lint` in `frontend`.
- [ ] Run `npm run build` in `frontend`.
- [ ] Start backend/frontend if needed and smoke-check the UI in a browser.
- [ ] Commit with a direct message and no co-author metadata.
