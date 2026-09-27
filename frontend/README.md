# AI Mentors — Frontend

React 19 + Vite + Tailwind CSS 4 client for the AI Mentors app.

## Setup

```bash
npm install
```

Create `frontend/.env` (see `.env.example` if present):

```env
VITE_API_URL=http://localhost:8000
```

```bash
npm run dev      # start dev server
npm run build    # production build
npm run lint     # eslint
```

## Talking to the Backend

All API calls go through `src/services/api.js`:

- `baseURL` comes from `VITE_API_URL`
- 60s timeout (LLM responses can be slow)
- `getFriendlyErrorMessage(error)` maps any failure — network down, timeout, backend
  `{"detail": "..."}` — to a user-facing message shown as a mentor bubble in the chat

**Mentor ids must match `backend/mentors/*.json`** — they're defined in
`src/data/mentors.js` and sent as `mentor_id` to `POST /chat`.

## Routes

| Path | Page |
|---|---|
| `/` | Mentor grid |
| `/chat/:id` | Chat with a specific mentor |
| `/about` | About the mentors |
