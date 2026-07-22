<div align="center">
  <img src="https://img.shields.io/badge/python-3.11+-6b4de6?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/fastapi-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/tests-28%20passed-success?style=flat-square&logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/license-MIT-blueviolet?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/release-v0.2.0-7c5cfc?style=flat-square" alt="Release">
</div>

<br>

```
╔══════════════════════════════════════════════════════════╗
║  ◆  H A L L U C I N A T I O N   L E D G E R            ║
║     Extract · Track · Verify · Export                   ║
╚══════════════════════════════════════════════════════════╝
```

<p align="center">
  <strong>Paste LLM output → get atomic claims → classify each one → know which models lie.</strong><br>
  <sub>A forensic toolkit for auditing factual claims in AI-generated text. AI Safety · Day 002.</sub>
</p>

---

## Why

AI models fabricate with complete confidence — wrong dates, invented statistics, nonexistent people. If you rely on AI outputs where facts matter, you need to know which claims hold up. This tool gives you that answer.

---

## Quick Start

```bash
git clone https://github.com/natanaheldr/hallucination-ledger.git
cd hallucination-ledger
pip install -r requirements.txt
python run.py
```

Open **http://localhost:8000** → click **"Load demo data"** to see the dashboard populated instantly.

---

## How It Works

1. **Paste** an AI response → the engine extracts every verifiable factual statement
2. **Score** — each claim gets a confidence rating based on factual density
3. **Classify** — mark each as `verified`, `doubtful`, or `false` (hallucination)
4. **Analyze** — the dashboard shows which models hallucinate the most
5. **Export** — download your ledger as CSV or JSON

---

## Features

| Category | Details |
|----------|---------|
| **Claim Extraction** | 15 heuristic patterns detect dates, numbers, proper names, superlatives, citations |
| **Confidence Score** | 0.0–1.0 rating per claim based on factual indicator density |
| **Classification** | 4 statuses: verified · doubtful · hallucination · unreviewed |
| **Audit Trail** | Every status change logged with timestamp — full history per claim |
| **Bulk Operations** | Select multiple claims, reclassify all at once |
| **Per-Model Stats** | Hallucination rate per AI model with visual breakdown bars |
| **Search & Filter** | Full-text search + filter by status or model |
| **Export** | CSV for spreadsheets, JSON for programmatic use |
| **Themes** | Dark & light mode, persisted across sessions |
| **Shortcuts** | `F` search, `N` new, arrows paginate, `Ctrl+E` CSV, `Ctrl+J` JSON |

---

## API Reference

<details>
<summary><strong>17 endpoints — click to expand</strong></summary>
<br>

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Dashboard |
| `GET` | `/add` | Submission form |
| `GET` | `/claims/{id}` | Claim detail + audit trail |
| `GET` | `/api/claims` | List claims (paginated, `status`, `search`, `source_id`) |
| `POST` | `/api/claims` | Create claim |
| `POST` | `/api/claims/extract` | Paste response → auto-extract claims |
| `PATCH` | `/api/claims/{id}/status` | Update status (creates audit entry) |
| `POST` | `/api/claims/bulk-status` | Batch update multiple claims |
| `GET` | `/api/claims/{id}/audits` | Full status change history |
| `DELETE` | `/api/claims/{id}` | Remove claim |
| `GET` | `/api/claims/export?format=csv\|json` | Export filtered claims |
| `GET` | `/api/sources` | List AI model sources |
| `POST` | `/api/sources` | Register new source |
| `GET` | `/api/sources/{id}` | Source detail |
| `DELETE` | `/api/sources/{id}` | Delete source + claims |
| `GET` | `/api/sources/stats` | Per-model statistics + hallucination rates |
| `GET` | `/api/seed-demo` | Load 25 demo claims from 5 real AI models |

</details>

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| Framework | FastAPI + Uvicorn |
| Database | SQLite + SQLAlchemy 2.0 ORM |
| Validation | Pydantic v2 |
| Frontend | Jinja2 + Vanilla JS · zero framework overhead |
| CSS | Custom properties · dark/light themes · responsive |
| Testing | pytest · 28 tests · in-memory SQLite |
| Linting | ruff |

---

## Project Layout

<details>
<summary><strong>File tree — click to expand</strong></summary>
<br>

```
hallucination-ledger/
├── app/
│   ├── main.py                  FastAPI entry point
│   ├── database.py              SQLAlchemy engine & sessions
│   ├── models.py                ORM: Claim, ResponseSource, ClaimAudit
│   ├── schemas.py               Pydantic models with validators
│   ├── seed_demo.py             25 demo claims from 5 AI models
│   ├── routers/
│   │   ├── claims.py            CRUD, extract, bulk, export, audits
│   │   └── sources.py           CRUD, per-model statistics
│   ├── services/
│   │   ├── claim_extractor.py   Multi-pattern heuristic engine
│   │   └── export_service.py    CSV & JSON formatters
│   ├── static/
│   │   └── style.css            Full theme system
│   └── templates/
│       ├── base.html            Shell, nav, theme toggle
│       ├── index.html           Dashboard + bulk ops
│       ├── add_response.html    Submission form
│       └── claim_detail.html    Claim view + audit timeline
├── tests/
│   ├── conftest.py              In-memory SQLite fixtures
│   ├── test_claims.py           18 API tests
│   ├── test_export.py           Export unit tests
│   └── test_extractor.py        Extraction unit tests
├── .github/workflows/ci.yml     CI pipeline
├── requirements.txt
├── run.py
├── CHANGELOG.md
└── README.md
```

</details>

---

## Testing

```bash
pytest -v                   # 28 tests, all pass
ruff check .                # zero lint errors
```

No database setup needed — tests use in-memory SQLite.

---

## Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Write tests, run `ruff check . && pytest -v`
4. Open a PR against `main`

---

## License

MIT — use freely, attribution appreciated.

<br>

<p align="center">
  <sub>Built for transparency in the age of generated text.</sub>
</p>
