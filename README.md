<div align="center">
  <img src="https://img.shields.io/badge/python-3.11+-6b4de6?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/fastapi-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/tests-28%20passed-success?style=for-the-badge" alt="Tests">
  <img src="https://img.shields.io/badge/license-MIT-blueviolet?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge" alt="Status">
</div>

<br>

<h1 align="center">
  &#9670; Hallucination Ledger
</h1>

<p align="center">
  <strong>Extract, track, and verify factual claims buried inside AI-generated text.</strong>
</p>

<p align="center">
  A lightweight forensic tool for anyone who needs to know whether an LLM told the truth.
</p>

---

## Why this exists

Large language models sound authoritative even when they are completely wrong. They fabricate dates, invent statistics, misattribute quotes, and hallucinate entire events with unsettling confidence.

**Hallucination Ledger** helps you fight back. You paste an AI response, it pulls out every verifiable factual statement, and then you mark each one as *verified*, *doubtful*, or *false*. Over time you build a searchable, filterable record of exactly how reliable each model really is.

## What it does

- **Smart claim extraction** — Heuristic analysis identifies sentences that contain dates, numbers, proper names, superlatives, and other markers of factual assertions.
- **Confidence scoring** — Each extracted claim gets a numerical score estimating how many factual indicators it carries.
- **Four-way classification** — Mark claims as `verified`, `doubtful`, `false` (hallucination), or leave them `unreviewed`.
- **Full audit trail** — Every status change is recorded with a timestamp, so you can see the lifecycle of each claim.
- **Bulk operations** — Select multiple claims and update their status in one click.
- **Per-model analytics** — See which AI models hallucinate the most, with visual breakdowns and hallucination rates.
- **Search and filter** — Full-text search across all claims, filter by status or model.
- **Export** — Download your ledger as CSV or JSON for external analysis.

## Quick start

```bash
# Clone the repository
git clone https://github.com/natanaheldr/hallucination-ledger.git
cd hallucination-ledger

# Install dependencies
pip install -r requirements.txt

# Launch the application
python run.py
```

Open your browser and navigate to **[http://localhost:8000](http://localhost:8000)**.

## How to use

1. Go to **Analyze Response** and paste an AI model's output.
2. Enter the model name (e.g. `GPT-4o`, `Claude 3.5 Sonnet`).
3. Click **Extract Claims** — the system breaks the text into individual factual statements.
4. Visit the **Dashboard** to review each claim.
5. For each claim, select **Verified**, **Doubtful**, or **Hallucination**.
6. Watch the statistics update in real time as you classify claims.
7. Export your ledger anytime for reports or sharing.

## API reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Dashboard with paginated claims table |
| `GET` | `/add` | Form to paste and analyze AI responses |
| `GET` | `/claims/{id}` | Detailed view of a single claim |
| `GET` | `/api/claims?page=&status=&search=&source_id=` | List claims with filtering |
| `POST` | `/api/claims` | Create a single claim manually |
| `POST` | `/api/claims/extract` | Paste a response and auto-extract all claims |
| `PATCH` | `/api/claims/{id}/status` | Update the status of one claim |
| `POST` | `/api/claims/bulk-status` | Batch-update multiple claims at once |
| `GET` | `/api/claims/{id}/audits` | View the audit trail for a claim |
| `DELETE` | `/api/claims/{id}` | Remove a claim |
| `GET` | `/api/claims/export?format=csv\|json` | Export filtered claims |
| `GET` | `/api/sources` | List all AI model sources |
| `POST` | `/api/sources` | Register a new model source |
| `GET` | `/api/sources/{id}` | Get details about a source |
| `DELETE` | `/api/sources/{id}` | Delete a source and its claims |
| `GET` | `/api/sources/stats` | Aggregate statistics across all models |

## Project structure

```
hallucination-ledger/
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── database.py                 # SQLAlchemy engine and session management
│   ├── models.py                   # ORM models: Claim, ResponseSource, ClaimAudit
│   ├── schemas.py                  # Pydantic validation schemas
│   ├── routers/
│   │   ├── claims.py               # All /api/claims endpoints
│   │   └── sources.py              # All /api/sources endpoints
│   ├── services/
│   │   ├── claim_extractor.py      # Heuristic claim extraction engine
│   │   └── export_service.py       # CSV and JSON export formatters
│   ├── static/
│   │   └── style.css               # Complete dark-theme stylesheet
│   └── templates/
│       ├── base.html               # Shared layout and navigation
│       ├── index.html              # Main dashboard with bulk operations
│       ├── add_response.html       # AI response submission form
│       └── claim_detail.html       # Single claim view with audit history
├── tests/
│   ├── conftest.py                 # Pytest fixtures with in-memory SQLite
│   ├── test_claims.py              # API endpoint tests (18 tests)
│   ├── test_export.py              # Export service tests
│   └── test_extractor.py           # Claim extraction unit tests
├── .github/workflows/ci.yml        # CI pipeline with linting and tests
├── requirements.txt                # Python dependencies
├── run.py                          # Uvicorn launcher
└── README.md
```

## Running the tests

```bash
pytest -v
```

All 28 tests run against an in-memory SQLite database, so no external setup is needed.

## Tech stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Web framework | FastAPI |
| Server | Uvicorn |
| Database | SQLite (via SQLAlchemy ORM) |
| Validation | Pydantic v2 |
| Frontend | Jinja2 templates + vanilla JavaScript |
| Styling | Custom CSS with CSS custom properties |
| Testing | pytest, pytest-asyncio |
| Linting | ruff |

## License

This project is released under the [MIT License](LICENSE). Use it freely, modify it, and contribute back if you find it useful.

---

<p align="center">
  <sub>Built for transparency in the age of generated text.</sub>
</p>
