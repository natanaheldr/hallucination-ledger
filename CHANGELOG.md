# Changelog

All notable changes to the Hallucination Ledger project.

## [0.2.0] — Recent

### Added
- Demo data seeder with 25 pre-classified claims from 5 popular AI models (GPT-4o, Claude 3.5, Gemini 1.5 Pro, Claude 3 Opus)
- Bulk status update API endpoint for updating multiple claims at once
- Claim audit trail retrieval endpoint
- Source CRUD endpoints with nested claim statistics
- Confidence scoring for extracted claims based on factual indicator density
- Dark and light theme system with localStorage persistence
- Keyboard shortcuts for efficient navigation (F, N, arrows, Ctrl+E, Ctrl+J)
- Toast notification system for user feedback
- Per-model hallucination rate calculation in statistics
- Extended metadata fields: verification method, confidence score
- Per-page total count in pagination response

### Changed
- Completely redesigned dark theme with neon accent colors, Inter + JetBrains Mono fonts
- Enhanced heuristic claim extraction with 15 pattern categories and confidence scoring
- Improved sentence splitting for better claim boundary detection
- Year pattern expanded to match 1800–2099 range
- Database models now include performance indexes on status, source_id, and created_at
- Claims schema now includes confidence, verification method, and computed total_pages
- Statistics endpoint returns verified/false percentages and per-model hallucination rates
- CI workflow changed to manual dispatch only (avoids false failures from GitHub Actions billing lock)

### Fixed
- Route ordering bug where `/api/sources/stats` was captured by `/{source_id}` parameter
- Year 1889 not matching the regex pattern in claim extractor
- Removed unused imports across the codebase

## [0.1.0] — Initial Release
- FastAPI application with SQLite backend
- Heuristic claim extraction from AI-generated text
- Claim classification (verified, doubtful, false, unreviewed)
- Paginated, searchable, filterable claims dashboard
- CSV and JSON export
- Response source tracking per AI model
- Audit trail for every status change
- In-memory SQLite test suite
