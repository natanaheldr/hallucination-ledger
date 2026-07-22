# Hallucination Ledger

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/fastapi-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square" alt="Tests">
  <img src="https://img.shields.io/badge/license-MIT-purple?style=flat-square" alt="License">
</p>

<p align="center">
  <strong>Extract factual claims from AI responses and track which are verified, doubtful, or false.</strong>
</p>

---

## The Problem

AI language models generate plausible-sounding but factually incorrect statements (hallucinations). There's no systematic way to log these claims, tag their verification status, and track patterns over time.

## The Solution

**Hallucination Ledger** lets you paste an AI response, automatically extracts atomic factual claims, then lets you mark each claim as verified, doubtful, or false — building a searchable ledger of model reliability.

## Features

- **Auto-Extraction** — Paste AI responses, claims are automatically identified using heuristic analysis
- **Classification** — Mark claims as verified, doubtful, or false with full audit trail
- **Dashboard** — Searchable, filterable table with color-coded status badges
- **Model Tracking** — Group claims by model to see which hallucinates most
- **Export** — Download filtered claims as CSV or entire ledger as JSON
- **Statistics** — Per-model breakdown of verified vs false claims

## Quick Start

```bash
pip install -r requirements.txt
python run.py
```

Open [http://localhost:8000](http://localhost:8000)

## Running Tests

```bash
pytest -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard |
| GET | `/add` | Submission form |
| GET | `/claims/{id}` | Claim detail |
| GET | `/api/claims` | List claims (paginated, filterable) |
| POST | `/api/claims` | Create single claim |
| POST | `/api/claims/extract` | Paste response, extract claims |
| PATCH | `/api/claims/{id}/status` | Update claim status |
| DELETE | `/api/claims/{id}` | Delete claim |
| GET | `/api/claims/export?format=csv\|json` | Export claims |
| GET | `/api/sources` | List response sources |
| GET | `/api/sources/stats` | Summary statistics |

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Database:** SQLite via SQLAlchemy ORM
- **Frontend:** Jinja2 + Vanilla JavaScript
- **Testing:** pytest, pytest-asyncio

## License

MIT — see [LICENSE](LICENSE)
