# Hallucination Ledger — Day 002

## 1. Project Identity
- **Name:** Hallucination Ledger
- **Day:** 002
- **Category:** AI Safety / Fact-Checking
- **Tagline:** Extract factual claims from AI responses and track which are verified, doubtful, or false.

## 2. Overview & Problem Statement
AI language models frequently generate plausible-sounding but factually incorrect statements (hallucinations). There is no systematic, lightweight way to log these claims, tag their verification status, and track patterns over time. This tool lets you paste an AI response, automatically extracts atomic factual claims from it, then lets you mark each claim as verified, doubtful, or false — building a searchable ledger of model reliability.

## 3. Exact Tech Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI with Uvicorn
- **Database:** SQLite (via SQLAlchemy ORM)
- **API Client:** httpx (async)
- **Frontend:** Jinja2 templates + vanilla JavaScript (no heavy JS framework)
- **Styling:** Simple CSS (no framework dependency)
- **Testing:** pytest + pytest-asyncio + httpx (TestClient)
- **Package Manager:** pip / requirements.txt

## 4. Detailed Feature Requirements

### 4.1 Claim Extraction
- User pastes an AI-generated text response into a textarea.
- The backend splits the text into sentences, then uses keyword/heuristic analysis to extract claims:
  - Sentences containing factual assertions (dates, names, numbers, superlatives, "is/are/was" statements).
  - Each claim is stored as a separate `Claim` record.
- Alternatively, users can manually add claims one by one.

### 4.2 Claim Classification
- Each claim has a status: `unreviewed`, `verified`, `doubtful`, `false`.
- Users can bulk-update statuses via checkboxes or individually.
- Each status change is timestamped in an audit log (`ClaimAudit` table).
- Claims can have a `source_url` field pointing to verification evidence.

### 4.3 Ledger Dashboard
- Paginated table of all claims sorted by creation date (newest first).
- Filter by: status, source (which AI model), date range.
- Search bar for full-text search across claim content.
- Color coding: green (verified), yellow (doubtful), red (false), gray (unreviewed).
- Summary statistics bar: total claims, verified %, false %, unreviewed count.

### 4.4 Model Source Tracking
- When submitting a response, tag it with: model name (e.g. "GPT-4o", "Claude 3.5"), prompt used (optional), date.
- Dashboard can group claims by model to show which model hallucinates most.

### 4.5 Export
- Export filtered claims as CSV.
- Export entire ledger as JSON (for backup/portability).

## 5. Architecture & Folder Structure
```
day-002-hallucination-ledger/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── models.py            # ORM models: Claim, ClaimAudit, ResponseSource
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── claims.py        # CRUD endpoints for claims
│   │   └── sources.py       # Endpoints for response sources
│   ├── services/
│   │   ├── __init__.py
│   │   ├── claim_extractor.py   # Heuristic claim extraction logic
│   │   └── export_service.py    # CSV/JSON export logic
│   ├── static/
│   │   └── style.css        # Minimal custom styling
│   └── templates/
│       ├── base.html         # Base layout with Jinja2
│       ├── index.html        # Main dashboard
│       ├── add_response.html # Form to paste AI response
│       └── claim_detail.html # Single claim detail view
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Fixtures: test DB, test client
│   ├── test_claims.py        # CRUD endpoint tests
│   ├── test_extractor.py     # Claim extraction unit tests
│   └── test_export.py        # Export endpoint tests
├── requirements.txt
├── run.py                    # Simple uvicorn launcher
├── .env.example              # Template for env vars
└── README.md
```

## 6. Component Tree / Module Breakdown
```
FastAPI App
├── / (GET) → index.html (Dashboard)
├── /add (GET/POST) → add_response.html (Form)
├── /claims/{id} (GET) → claim_detail.html
├── /api/claims (GET) → List claims (with filters, pagination)
├── /api/claims (POST) → Create claim(s) from text
├── /api/claims/{id}/status (PATCH) → Update claim status
├── /api/claims/export (GET) → Export as CSV/JSON
├── /api/sources (GET/POST) → Manage response sources
└── /api/stats (GET) → Summary statistics JSON
```

## 7. Data Models / Schemas

### SQLAlchemy Models
```python
class ResponseSource(Base):
    __tablename__ = "response_sources"
    id: int (PK, autoincrement)
    model_name: str              # e.g. "GPT-4o"
    prompt: str (nullable)       # The prompt that generated the response
    raw_text: str                # The full original AI response
    created_at: datetime

class Claim(Base):
    __tablename__ = "claims"
    id: int (PK, autoincrement)
    source_id: int (FK → response_sources.id, nullable)
    claim_text: str              # The extracted claim sentence
    status: str                  # 'unreviewed' | 'verified' | 'doubtful' | 'false'
    source_url: str (nullable)   # URL to verification evidence
    notes: str (nullable)        # Free-text annotation
    created_at: datetime
    updated_at: datetime

class ClaimAudit(Base):
    __tablename__ = "claim_audits"
    id: int (PK, autoincrement)
    claim_id: int (FK → claims.id)
    old_status: str
    new_status: str
    changed_at: datetime
```

### Pydantic Schemas
```python
class ClaimCreate(BaseModel):
    source_id: int | None = None
    claim_text: str

class ClaimStatusUpdate(BaseModel):
    status: Literal['unreviewed', 'verified', 'doubtful', 'false']
    source_url: str | None = None
    notes: str | None = None

class ExtractRequest(BaseModel):
    raw_text: str
    model_name: str
    prompt: str | None = None

class ClaimsResponse(BaseModel):
    claims: list[ClaimOut]
    total: int
    page: int
    per_page: int

class StatsResponse(BaseModel):
    total: int
    verified: int
    doubtful: int
    false_count: int
    unreviewed: int
    by_model: dict[str, dict]  # model_name → { verified, false, total }
```

## 8. API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard HTML |
| GET | `/add` | Submission form HTML |
| GET | `/claims/{id}` | Claim detail HTML |
| GET | `/api/claims` | Paginated claims list (?status=, ?search=, ?source_id=, ?page=, ?per_page=) |
| POST | `/api/claims` | Create single claim |
| POST | `/api/claims/extract` | Paste response, extract claims, store all |
| PATCH | `/api/claims/{id}/status` | Update claim status |
| DELETE | `/api/claims/{id}` | Delete a claim |
| GET | `/api/claims/export` | Export (?format=csv|json) |
| GET | `/api/stats` | Summary statistics |
| GET | `/api/sources` | List response sources |

## 9. Step-by-Step Implementation Guide

### Phase 1 — Scaffolding (Steps 1-3)
1. Create directory structure, write `requirements.txt` with: `fastapi, uvicorn, sqlalchemy, pydantic, httpx, jinja2, python-multipart, pytest, pytest-asyncio, httpx`.
2. Write `app/database.py` — create SQLAlchemy engine bound to `sqlite:///./hallucination_ledger.db`, sessionmaker, `get_db()` dependency, `Base` declarative base.
3. Write `app/models.py` — define `ResponseSource`, `Claim`, `ClaimAudit` with relationships (`source.claims`, `claim.audits`).

### Phase 2 — Services (Steps 4-5)
4. Write `app/services/claim_extractor.py`:
   - `extract_claims(text: str) -> list[str]`: split on `. `, `! `, `? `; filter sentences that contain factual indicators (numbers, proper nouns capitalized mid-sentence, dates in YYYY format, comparative adjectives like "first"/"largest"/"only").
   - Add a `classify_initial_status(claim_text: str) -> str`: always returns "unreviewed".
5. Write `app/services/export_service.py`:
   - `export_csv(claims: list[Claim]) -> str`: generate CSV with columns: id, claim_text, status, model_name, created_at.
   - `export_json(claims: list[Claim]) -> str`: serialize to JSON.

### Phase 3 — API Routes (Steps 6-8)
6. Write `app/routers/claims.py` — all CRUD endpoints for claims with pagination, filtering, status updates that also create `ClaimAudit` records.
7. Write `app/routers/sources.py` — CRUD for response sources, list endpoint.
8. Write `app/schemas.py` — all Pydantic models for request/response validation.

### Phase 4 — Frontend (Steps 9-12)
9. Write `app/templates/base.html` — HTML5 boilerplate with nav bar, flash messages area, script block.
10. Write `app/templates/index.html` — dashboard table with filters, stats cards (green/yellow/red/gray), export buttons, pagination links.
11. Write `app/templates/add_response.html` — form with textarea, model name input, prompt input, "Extract Claims" submit.
12. Write `app/static/style.css` — minimal styling: table borders, status badges with colors, responsive layout.

### Phase 5 — App Assembly (Steps 13-14)
13. Write `app/main.py` — create FastAPI app, mount static files, include routers, add startup event to create tables with `Base.metadata.create_all`.
14. Write `run.py` — `uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)`.

### Phase 6 — Testing (Step 15)
15. Write all tests detailed in section 10.

## 10. Testing Requirements
- **test_extractor.py:** Test `extract_claims()` with known sentences — verify it correctly identifies factual sentences, test with empty string, test with pure opinion text (should return few/no claims).
- **test_claims.py:** Test POST `/api/claims/extract` creates claims and source record. Test GET `/api/claims` returns paginated results. Test PATCH status update creates audit log entry. Test DELETE removes claim. Test export endpoint returns valid CSV.
- **conftest.py:** Use an in-memory SQLite database for tests (`sqlite:///:memory:`), create all tables before each test module, provide `TestClient` fixture.

## 11. README Template
```markdown
# Hallucination Ledger (Day 002)

Track and classify factual claims in AI-generated text.

## Features
- Paste AI responses, auto-extract factual claims
- Mark claims as verified, doubtful, or false
- Full audit trail of status changes
- Search and filter by model, status, date
- Export ledger as CSV or JSON
- Summary statistics per model

## Quick Start
```bash
pip install -r requirements.txt
python run.py
```
Open http://localhost:8000

## Running Tests
```bash
pytest -v
```

## License
MIT
```

## 12. GitHub Actions Config
`.github/workflows/ci.yml`:
- Trigger: push to main, PRs.
- Steps: checkout, setup Python 3.11, `pip install -r requirements.txt`, `pytest -v`, `ruff check .`.

## 13. Definition of Done Checklist
- [ ] User can paste AI response text and auto-extract claims.
- [ ] Claims appear in paginated, filterable, searchable table.
- [ ] Each claim can be marked verified/doubtful/false.
- [ ] Status changes are audited (ClaimAudit records created).
- [ ] Summary statistics display correctly.
- [ ] Export CSV and JSON work.
- [ ] Search across claim text works.
- [ ] Filter by model/source works.
- [ ] All tests pass with `pytest -v`.
- [ ] No hardcoded credentials or secrets.
- [ ] `pip install -r requirements.txt && python run.py` starts the app.

## 14. Installation & Run Commands
```bash
pip install -r requirements.txt
python run.py                # Start server
pytest -v                    # Run tests
pytest --cov=app --cov-report=html   # Coverage (if pytest-cov installed)
```

## 15. Rules
- **NO secrets in code.** Database is local SQLite; no API keys needed.
- **Include MIT LICENSE file.**
- **Include error handling:** 404 for missing claims, 400 for invalid input, 500 catch-all with detail in dev mode.
- **Single command startup:** `pip install -r requirements.txt && python run.py`.
- All forms must have CSRF protection via FastAPI's built-in form handling (or a simple token check).
- SQL injection prevention via SQLAlchemy ORM parameterization.
