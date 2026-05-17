# Frontend

SvelteKit chat UI for the LangChain Property Appraiser backend.

## Local development

Start the backend first from the repository root:

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/uvicorn app.main:app --reload
```

Then run the frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend calls the backend `/chat` endpoint. Override the backend URL with:

```bash
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

## Structure

- `src/routes/+page.svelte` keeps the initial chat layout and local state.
- `src/lib/api/chat.ts` contains the simple backend API call.

No global state manager is used in V1.
