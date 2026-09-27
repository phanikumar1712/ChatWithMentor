# AI Mentors 🕉️

Chat with AI personas of great mentors — Lord Krishna, Lord Rama, Lord Hanuman, Baahubali, Bhagat Singh, Einstein, Kalam, Gandhi, and Swami Vivekananda. RAG-enabled mentors answer from their own teachings (Bhagavad Gita, Ramayana) retrieved from a local Chroma vector store.

## Features

- 🧠 **9 mentor personas** with individual prompts, tone, and values
- 📚 **RAG (Retrieval-Augmented Generation)** for Krishna, Rama, and Baahubali — grounded in their source texts
- 💬 **Per-mentor conversation memory** with a reset endpoint
- 🛡️ **NeMo Guardrails** — input/output safety rails with fail-open semantics
- 🧯 **Graceful error handling** end-to-end (specific LLM errors → friendly messages)
- ⚛️ **React + Vite + Tailwind** frontend with themed chat backgrounds

## Project Structure

```
├── backend/                 # FastAPI + LangChain API
│   ├── app.py               # Endpoints: /, /chat, /reset-memory/{mentor_id}
│   ├── chains/              # mentor_chain (LLM + memory), rag_chain, chain_router, guardrails
│   ├── config/guardrails/   # NeMo Guardrails config.yml + self-check prompts.yml
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

## Guardrails (NeMo Guardrails)

`/chat` runs two safety layers from `chains/guardrails.py` before and after the LLM call. Each layer combines an LLM self-check with a deterministic regex rail (`config/guardrails/config.yml`):

1. **Input rails** —
   - *regex check input*: 16 deterministic patterns for prompt injection ("ignore all previous instructions", "disregard your rules"...), system-prompt extraction, and jailbreak tokens (DAN mode, "do anything now", `<|im_start|>` spoofing, "BEGIN SYSTEM MODE"). No LLM call, instant block.
   - *self check input*: LLM screen against the policy in `prompts.yml` (harm, self-harm, explicit content, abuse, semantic jailbreaks that regex can't catch). Blocked → polite refusal, HTTP 200.
2. **Output rails** —
   - *regex check output*: blocks leaking API keys (`sk-or-v1-...`, `ghp_...`), private keys, emails, SSNs, card numbers, phone numbers, IBANs.
   - *self check output*: LLM screen for harmful instructions and system-prompt/passage leaks. Blocked → safe replacement message, HTTP 200.

> Why not NeMo's built-in `jailbreak detection heuristics` (GPT-2-large perplexity) or `sensitive data detection` (Presidio + spaCy `en_core_web_lg`)? Both need ~1.5GB+ of extra models for marginal gain — the regex rails deterministically cover the same attack classes here. To upgrade later: `pip install presidio-analyzer presidio-anonymizer && python -m spacy download en_core_web_lg`, then add `detect sensitive data on input` to `rails.input.flows`.

Behavior & configuration:

| Env var | Default | Meaning |
|---|---|---|
| `GUARDRAILS_ENABLED` | `true` | Set `false` to bypass rails entirely |
| `GUARDRAILS_TIMEOUT` | `10` | Seconds before a rail check gives up and allows the message |

**Fail-open philosophy:** if the rails engine fails to initialize, crashes, or times out, messages are *allowed through* and the error is logged — the persona prompts in `backend/prompts/safety.txt` remain the inner safety layer. The self-check rails reuse the same OpenRouter LLM as the chat (temperature 0).

Test suites (scripted fake LLM, no API key needed):

```bash
cd backend
./venv/bin/python tests/test_guardrails.py     # 10 cases: rail mechanics, fail-open, endpoint-level
./venv/bin/python tests/test_attack_cases.py   # 43 cases: injection, jailbreak tokens, PII leaks, false positives
```

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
