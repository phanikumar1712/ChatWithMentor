# AI Mentors 🕉️

Chat with AI personas of great mentors — Lord Krishna, Lord Rama, Lord Hanuman, Baahubali, Bhagat Singh, Einstein, Kalam, Gandhi, and Swami Vivekananda. RAG-enabled mentors answer from their own teachings (Bhagavad Gita, Ramayana) retrieved from a local Chroma vector store.

## Features

- 🧠 **9 mentor personas** with individual prompts, tone, and values
- 📚 **RAG (Retrieval-Augmented Generation)** for Krishna, Rama, and Baahubali — grounded in their source texts
- 💬 **Per-mentor conversation memory** with a reset endpoint
- 🛡️ **Safety prompt layer** + graceful error handling end-to-end
- ⚛️ **React + Vite + Tailwind** frontend with themed chat backgrounds

## Project Structure

```
├── backend/                 # FastAPI + LangChain API
│   ├── app.py               # Endpoints: /, /chat, /reset-memory/{mentor_id}
│   ├── chains/              # mentor_chain (LLM + memory), rag_chain, chain_router
│   ├── mentors/             # Mentor persona configs (JSON)
│   ├── prompts/             # base / safety / persona prompt files
│   ├── rag/
│   │   ├── books/           # Source texts (gita.txt, ramayana.txt, baahubali.txt)
│   │   ├── db/              # Generated Chroma vector stores (gitignored)
│   │   └── build_index.py   # Builds the vector DBs
│   ├── schemas/             # Pydantic request/response models
│   └── utils/               # mentor_loader, prompt_builder, retriever_factory
└── frontend/                # React + Vite client
    └── src/
        ├── components/      # Chat, mentor grid, header components
        ├── pages/           # ChatPage, AboutMentors
        ├── services/api.js  # Axios instance + friendly error mapping
        └── data/mentors.js  # Mentor ids (must match backend/mentors/*.json)
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai/keys) API key

## Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
OPENAI_API_KEY=sk-or-v1-your-real-openrouter-key
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-3.5-turbo
```

> ⚠️ The key must be a real OpenRouter key (`sk-or-v1-...`). A placeholder key causes
> every `/chat` request to fail with `401 Missing Authentication header`.

**Build the RAG vector stores** (required for Krishna, Rama, Baahubali):

```bash
python rag/build_index.py
# ✅ Vector DB built for krishna / rama / baahubali
```

**Run the API**:

```bash
uvicorn app:app --reload --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

**Run the dev server**:

```bash
npm run dev
```

## API Reference

Base URL: `http://localhost:8000`

### `GET /`
Health check → `{"message": "AI Mentor backend running"}`

### `POST /chat`
```json
{ "mentor_id": "krishna", "user_message": "What is my duty?" }
```
→ `200 {"reply": "..."}`

Errors (all return `{"detail": "<friendly message>"}`):

| Status | Cause |
|---|---|
| 422 | Missing/invalid `mentor_id` or `user_message` (1–4000 chars) |
| 429 | LLM provider rate limit |
| 500 | Unexpected server error (logged server-side) |
| 502 | LLM auth rejected, model denied, or provider error |
| 504 | LLM timeout or unreachable |

### `POST /reset-memory/{mentor_id}`
Clears that mentor's in-memory conversation history → `{"status": "memory cleared"}`

## How RAG Works Here

1. `rag/build_index.py` chunks each book and embeds it into `rag/db/<mentor>_chroma` using `all-MiniLM-L6-v2`
2. On `/chat`, mentors with `"rag_enabled": true` get their retriever from `utils/retriever_factory.py`
3. The top-3 passages are appended to the user's message before the LLM call
4. If retrieval fails, it degrades silently to a normal chat

## Troubleshooting

| Symptom | Fix |
|---|---|
| Chat shows *"The AI service rejected its credentials"* | `OPENAI_API_KEY` in `backend/.env` is invalid/placeholder — create one at openrouter.ai/keys |
| Chat shows *"Cannot reach the mentor service"* | Backend not running, or `VITE_API_URL` missing/wrong in `frontend/.env` |
| RAG mentors answer without book knowledge | Run `python rag/build_index.py` (the `rag/db/` folder is generated, not committed) |
| Mentor 404-ish / generic persona | `mentor_id` must match a file in `backend/mentors/` (falls back to `default.json`) |
| Port 8000 busy | `uvicorn app:app --port 8001` and point `VITE_API_URL` at it |

## Scripts

| Location | Command | Purpose |
|---|---|---|
| backend | `uvicorn app:app --reload` | Run API |
| backend | `python rag/build_index.py` | Rebuild vector stores |
| frontend | `npm run dev` | Dev server |
| frontend | `npm run build` | Production build |
| frontend | `npm run lint` | ESLint |
