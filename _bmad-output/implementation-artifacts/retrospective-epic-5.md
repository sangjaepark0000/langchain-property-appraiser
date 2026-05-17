# Retrospective: Epic 5 Svelte Web Chat Experience

## Completed

- Minimal SvelteKit frontend skeleton and local dev docs.
- Chat input/message list components.
- `/chat` frontend integration with conversation id handling and error display.
- Citation/source panel rendering from backend response values only.
- Data mode and safety notices to avoid confusing sample/unknown data with official determinations.
- Loading/error/insufficient evidence status panel.
- Backend/frontend 3-turn smoke script without adding browser automation dependency.

## Validation

- Final Epic 5 validation: `cd backend && .venv/bin/pytest` → 141 passed on Story 5.7 branch before merge.

## Lessons

- Frontend static contract tests need stable test IDs even after component extraction.
- Until a frontend lockfile/test stack is introduced, Python smoke/static contract tests provide low-risk coverage.
- UI copy must consistently distinguish evidence insufficiency from API failure and sample data from official determinations.

## Follow-ups

- Add real frontend package install/build CI once lockfile policy is decided.
- Add browser automation for Story 5.7-equivalent behavior when Playwright/Vitest infrastructure is introduced.
