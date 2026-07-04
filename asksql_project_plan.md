# AskSQL — Text-to-SQL AI Assistant
### Project Plan (Portfolio / Resume Build, $0 stack)

---

## 1. What you're building

An app where a user types a plain-English question ("What were our top 5 products by revenue last quarter?") and gets back:
1. The generated SQL query
2. The real results, run against an actual database
3. (Optional) a chart of the results

The pitch, in one line for your resume: *"Built a full-stack RAG-based text-to-SQL assistant with schema-aware retrieval, LLM query generation, and safety guardrails — deployed end-to-end on a $0 cloud stack."*

---

## 2. Final tech stack (all free tiers, no credit card required)

| Layer | Tool | Why |
|---|---|---|
| LLM (query generation) | **Google Gemini 2.5 Flash API** (primary), **Groq** (backup/fast open models), **Ollama** (local dev) | 1,500 free requests/day on Gemini, no card; Groq for speed/variety; Ollama for unlimited local iteration |
| Agent / orchestration | **LangChain** | Open source, handles the retrieval → prompt → SQL → execute pipeline |
| Vector DB (schema RAG) | **Chroma** | Free, embeddable, no hosting cost |
| Embeddings | **sentence-transformers** (local) | Avoids paid OpenAI embedding calls |
| Database | **Neon (serverless Postgres)** | 100 CU-hrs/month free, scale-to-zero, no auto-pause issue like Supabase |
| Backend | **Python (FastAPI)** | Lightweight, async, plays well with LangChain |
| Frontend | **React** | Matches "production-grade" positioning; deploy free on Vercel |
| Backend hosting | **Render (free web service)** or **Hugging Face Spaces** | Genuinely free; HF Spaces doubles as a public portfolio link |
| Frontend hosting | **Vercel** | Free tier, one-click deploys from GitHub |
| Version control | **GitHub** | Free, also where recruiters will look |

**Total cost: $0/month**, bounded by daily API rate limits (fine for a demo).

---

## 3. Architecture (the RAG pipeline)

```
User question (plain English)
        │
        ▼
[1] Retrieve relevant schema (Chroma vector search over table/column
    descriptions) — solves "context window overflow" and "business
    meaning is lost" from the reference posts
        │
        ▼
[2] Build prompt: question + retrieved schema + few-shot examples
        │
        ▼
[3] LLM generates SQL (Gemini/Groq/Ollama)
        │
        ▼
[4] Guardrail layer — validate before execution:
    - Reject anything that isn't SELECT (no DROP/DELETE/UPDATE/INSERT)
    - Enforce row limits (e.g. LIMIT 500)
    - Query timeout
    - Basic SQL-injection / syntax sanity check
        │
        ▼
[5] Execute against Neon Postgres (read-only DB user)
        │
        ▼
[6] Return SQL + results (+ optional chart) to React frontend
```

This directly answers the "why typical solutions fail" list from the reference post — you're building the *fixes* for context overflow, lost business meaning, hallucinated SQL, and missing guardrails, not just a demo that ignores them.

---

## 4. Build phases

### Phase 0 — Setup (½ day)
- Create GitHub repo
- Sign up: Google AI Studio (Gemini key), Groq, Neon, Vercel, Render/HF Spaces
- Install Ollama locally, pull a small model (e.g. `llama3.1:8b`) for dev

### Phase 1 — Data layer (1 day)
- Decide on a **realistic business dataset** (this matters for the "real business use case" pitch). Good free options:
  - Classic sample DBs: Northwind, Chinook, or Pagila (all free, realistic schemas — sales, orders, customers)
  - Or a Kaggle dataset you reshape into a normalized schema yourself (shows more skill)
- Load it into Neon Postgres
- Write clear table/column descriptions (this becomes your RAG corpus in step 2)

### Phase 2 — Schema RAG (1–2 days)
- Embed table/column descriptions with sentence-transformers
- Store in Chroma
- Write the retrieval function: given a question, pull the top-k relevant tables/columns

### Phase 3 — SQL generation (2 days)
- Prompt engineering: schema + question + a few worked examples → SQL
- Wire up LangChain to call Gemini (primary) with Groq/Ollama as fallback
- Test against 15–20 hand-written questions of increasing difficulty (single table → joins → aggregations)

### Phase 4 — Guardrails (1 day)
- SELECT-only enforcement (parse/regex check before execution)
- Row limit injection
- Query timeout
- Read-only DB role in Neon (defense in depth, not just app-layer)
- Friendly error messages when the model produces something invalid, with one retry

### Phase 5 — Backend API (1 day)
- FastAPI endpoints: `POST /ask` → returns `{sql, results, explanation}`
- Wrap the whole pipeline behind it

### Phase 6 — Frontend (2 days)
- React chat-style UI: input box, SQL shown (syntax highlighted), results table, optional chart (e.g. with Recharts)
- Loading states, error states

### Phase 7 — Deploy (½–1 day)
- Backend → Render or HF Spaces
- Frontend → Vercel
- Environment variables (API keys) set as secrets, never committed

### Phase 8 — Polish for portfolio (1 day)
- README with architecture diagram, setup instructions, and a demo GIF
- Short demo video (30–60s) for LinkedIn
- Write a short blog post / LinkedIn post explaining the guardrails and RAG design decisions — this is often what actually gets recruiter attention, more than the repo itself

**Rough total: 9–12 focused days**, less if you're comfortable with FastAPI/React already.

---

## 5. What makes this stand out vs. the two reference posts

Both posts describe the *idea*. What will differentiate your build:
1. **Actually implemented guardrails** (most demo repos skip this — you can point to the exact code)
2. **Multi-provider LLM routing with local fallback** — shows cost/reliability awareness, a real engineering concern
3. **A written explanation of *why*** (schema RAG solves context overflow, guardrails solve safety) — turns a demo into evidence of understanding, not just following a tutorial

---

## 6. Open decisions for you

- **Dataset**: pick something recognizable (Northwind/Chinook) for quick setup, or a messier real-world Kaggle dataset if you want to show more data-modeling skill
- **Chart library**: Recharts is the natural pick given your React stack
- **Auth**: skip it entirely for a portfolio demo (adds no resume value, adds real work)

Let me know which dataset you want to go with and I can start scaffolding the actual code.
