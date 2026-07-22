<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-6b4de6?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Tests](https://img.shields.io/badge/tests-28%20passed-success?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)

<br>

```
  ╔══════════════════════════════════════════════════════════════╗
  ║  ◆  H A L L U C I N A T I O N   L E D G E R                ║
  ║     Extract · Track · Verify · Export                       ║
  ╚══════════════════════════════════════════════════════════════╝
```

<p>
  <strong>A forensic toolkit for auditing factual claims in AI-generated text.</strong><br>
  <sub>Paste LLM output → get atomic claims → classify each one → know which models lie.</sub>
</p>

</div>

---

## The Problem

AI models don't admit when they don't know something. Instead, they fabricate — with complete confidence. Dates that never happened, statistics pulled from nowhere, people who don't exist, events that never occurred. **Hallucination** is the industry's polite word for it.

If you use AI outputs in research, journalism, legal work, medicine, or any domain where facts matter, you need to know *which claims hold up and which don't*.

## What This Tool Does

<div align="center">

| Step | Action |
|:----:|--------|
| **1** | Paste an AI response into the analyzer |
| **2** | The engine extracts every verifiable factual claim |
| **3** | Each claim is scored for factual density (confidence) |
| **4** | You classify each claim: verified, doubtful, or hallucination |
| **5** | The dashboard reveals which models are most (and least) reliable |

</div>

### Core Capabilities

- **Heuristic Claim Extraction** — Detects sentences containing dates, statistics, proper names, superlatives, citations, and other markers of factual assertions. Not just regex — multi-pattern scoring.
- **Confidence Scoring** — Every extracted claim receives a numerical score (0.0–1.0) based on how many factual indicators it carries. Higher score = more specific, more verifiable.
- **Four-way Classification** — `verified` · `doubtful` · `false` (hallucination) · `unreviewed`. Each status change is logged in a permanent audit trail.
- **Bulk Operations** — Select multiple claims with checkboxes and update their status in one click. Sort, filter, and search across all claims.
- **Per-model Analytics** — Visual breakdown of hallucination rates per AI model. See at a glance whether GPT-4o, Claude, or Gemini is giving you the most fabrications.
- **Full Export** — Download your entire ledger as CSV for spreadsheet analysis or JSON for programmatic use.
- **Keyboard Shortcuts** — `F` to search, `N` for new analysis, arrow keys to paginate, `Ctrl+E`/`Ctrl+J` to export.
- **Dark & Light Themes** — Toggle between cinematic dark mode and clean light mode, persisted across sessions.

---

## Quick Start

```bash
git clone https://github.com/natanaheldr/hallucination-ledger.git
cd hallucination-ledger
pip install -r requirements.txt
python run.py
```

Open **[http://localhost:8000](http://localhost:8000)** — click **"Load demo data"** to see the dashboard with 25 pre-classified claims from 5 AI models immediately.

---

## How It Looks

> The dashboard presents a dark/light themed interface with:
> - **5 stat cards** at the top showing total, verified, doubtful, hallucination, and unreviewed counts with percentages
> - **Per-model breakdown bars** showing the proportion of verified vs hallucinated claims per AI model
> - **Search, filter, and bulk-select** controls in a unified toolbar
> - **Paginated claims table** with inline status selectors, confidence indicators, and one-click detail views
> - **Toast notifications** for every action (status updates, bulk operations, exports)
> - **Audit trail timeline** on each claim's detail page showing every status change

---

## API Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Dashboard with full interactive claims table |
| `GET` | `/add` | AI response submission and analysis form |
| `GET` | `/claims/{id}` | Detailed view of a single claim with audit trail |
| `GET` | `/api/claims` | List claims (paginated, filtered by `status`, `search`, `source_id`) |
| `POST` | `/api/claims` | Create a single claim manually |
| `POST` | `/api/claims/extract` | Paste AI response text, auto-extract all factual claims |
| `PATCH` | `/api/claims/{id}/status` | Update status of one claim (creates audit entry) |
| `POST` | `/api/claims/bulk-status` | Batch-update status for multiple claims at once |
| `GET` | `/api/claims/{id}/audits` | Retrieve the complete audit history for a claim |
| `DELETE` | `/api/claims/{id}` | Permanently remove a claim |
| `GET` | `/api/claims/export?format=csv\|json` | Export filtered claims |
| `GET` | `/api/sources` | List all AI model sources |
| `POST` | `/api/sources` | Register a new AI model source |
| `GET` | `/api/sources/{id}` | Get details about a specific source |
| `DELETE` | `/api/sources/{id}` | Delete a source and all its associated claims |
| `GET` | `/api/sources/stats` | Aggregate statistics with per-model hallucination rates |
| `GET` | `/api/seed-demo` | Populate the database with 25 realistic demo claims |

---

## Project Structure

```
hallucination-ledger/
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── database.py                 # SQLAlchemy engine, session, test helpers
│   ├── models.py                   # ORM models: Claim, ResponseSource, ClaimAudit
│   ├── schemas.py                  # Pydantic validation with field validators
│   ├── seed_demo.py                # Demo data seeder (5 models, 25 claims)
│   ├── routers/
│   │   ├── claims.py               # /api/claims — CRUD, extract, bulk, export, audits
│   │   └── sources.py              # /api/sources — CRUD, per-model statistics
│   ├── services/
│   │   ├── claim_extractor.py      # Multi-pattern heuristic claim detection engine
│   │   └── export_service.py       # CSV and JSON serialization formatters
│   ├── static/
│   │   └── style.css               # Complete CSS with dark/light themes
│   └── templates/
│       ├── base.html               # Shared layout, nav, theme toggle, shortcuts
│       ├── index.html              # Dashboard with bulk operations and interactive stats
│       ├── add_response.html       # AI response submission with extraction feedback
│       └── claim_detail.html       # Single claim view with audit history timeline
├── tests/
│   ├── conftest.py                 # Pytest fixtures (in-memory SQLite, TestClient)
│   ├── test_claims.py              # API endpoint tests (18 tests)
│   ├── test_export.py              # Export service unit tests
│   └── test_extractor.py           # Claim extraction unit tests
├── .github/workflows/ci.yml        # Manual + PR CI pipeline (lint + tests)
├── requirements.txt                # Python dependencies
├── run.py                          # Uvicorn launcher
└── README.md                       # You are here
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Language | **Python 3.11+** | Modern typing, pattern matching, performance |
| Framework | **FastAPI** | Auto-generated OpenAPI docs, async support, validation |
| Server | **Uvicorn** | Lightning-fast ASGI server with hot reload |
| Database | **SQLite** + **SQLAlchemy 2.0** | Zero-config persistent storage with full ORM |
| Validation | **Pydantic v2** | Type-safe request/response models with validators |
| Frontend | **Jinja2** + **Vanilla JS** | No framework overhead, server-rendered with progressive enhancement |
| Styling | **Custom CSS** | CSS custom properties for theming, zero dependencies |
| Testing | **pytest** | 28 tests, in-memory database, full API coverage |
| Linting | **ruff** | Blazing-fast Python linter written in Rust |

---

## Testing

```bash
# Run all 28 tests
pytest -v

# Run with coverage
pip install pytest-cov
pytest --cov=app --cov-report=term-missing

# Lint all Python files
ruff check .
```

All tests use an in-memory SQLite database — no external setup, no configuration, no cleanup needed.

---

## Contributing

Contributions are welcome. Here is how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-improvement`
3. **Write** tests for your changes
4. **Run** the full suite: `ruff check . && pytest -v`
5. **Commit** with clear, descriptive messages
6. **Open** a pull request against `main`

Keep the PR focused. Large, multi-feature PRs are harder to review.

---

## License

Released under the [MIT License](LICENSE). Use it, modify it, ship it, learn from it — just keep the attribution.

---

<div align="center">
  <br>
  <sub>Day 002 of the AI Safety Toolkit · Built for transparency in the age of generated text.</sub>
</div>
