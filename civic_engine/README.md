# Civic Issue Discovery, Intelligence, and Action Generation Engine

A production-oriented, provider-agnostic GenAI engine that discovers civic issues from publicly available information, cross-corroborates related reports across sources, detects chronic and recurring municipal defects, maps statutory accountability, and generates safe, practical volunteer opportunities.

---

## Key Features

- **Provider-Independent AI Architecture**: Common interface (`analyzeSource`, `extractCivicIssues`, `classifyIssue`, `findRelatedIssues`, `identifyStakeholders`, `generateCivicAction`, `evaluateEvidence`) supporting **Google Gemini API**, **OpenAI API**, **Anthropic Claude API**, and a **Deterministic Offline Mock Provider**.
- **Multi-Source Ingestion Pipeline**: Ingests public news articles, RSS/Atom syndication feeds, government PDFs, CSV grievance datasets, DOCX files, plain text, and citizen submissions.
- **SHA-256 Deduplication & Provenance**: Normalizes sources into a common format with cryptographic content hashing to ensure idempotent ingestion.
- **Hybrid Matching & Recurrence Engine**: Combines TF-IDF semantic similarity, spatial distance calculation via the Haversine formula, temporal delta tracking, and category compatibility to classify relationships into:
  - `DUPLICATE_REPORT` (same acute incident)
  - `RECURRING_INCIDENT` (chronic recurring problem)
  - `NEARBY_SIMILAR` (neighboring corridor)
  - `CROSS_AREA_SIMILAR` (separate zones)
  - `UNRELATED_KEYWORD_MATCH` (different categories)
- **Explainable Civic Intelligence Scoring**: Generates transparent, multi-factor scores for Severity (1-10), Urgency (1-10), Recurrence (1-10), Evidence Strength (1-10), Community Impact (1-10), and Actionability (1-10), with a composite Priority Score (0-100).
- **Statutory Authority Discovery & Anti-Hallucination**: Maps verified municipal departments, ward offices, and civil society organizations (pre-seeded with Mumbai BMC, TMC, NMMC, MPCB, and Praja Foundation). Never fabricates contact numbers or emails.
- **Civic Action & Volunteer Generator**: Produces step-by-step citizen action plans with explicit volunteer roles, required materials, and safety guardrails. High-risk actions are marked for human moderation.
- **Full REST API Layer**: Versioned endpoints under `/api/v1` for health, sources, issues, stakeholders, opportunities, reviews, and analytics with interactive OpenAPI / Swagger UI.

---

## Project Structure

```text
civic_engine/
├── app/
│   ├── api/v1/                # Versioned REST API routers
│   │   ├── health.py          # Health, safe configuration, job status
│   │   ├── sources.py         # Source ingestion & upload endpoints
│   │   ├── issues.py          # Issues, discovery, matching & evidence
│   │   ├── stakeholders.py    # Authority discovery endpoints
│   │   ├── opportunities.py   # Action generation & review endpoints
│   │   └── analytics.py       # Trends, categories & location analytics
│   ├── core/                  # Core configuration, database & security
│   │   ├── config.py          # Pydantic BaseSettings & env loader
│   │   ├── database.py        # SQLAlchemy 2.0 session & engine
│   │   ├── exceptions.py      # Custom exception hierarchy
│   │   └── security.py        # Prompt injection defense & SHA-256
│   ├── models/                # SQLAlchemy relational database models
│   ├── schemas/               # Strict Pydantic output validation schemas
│   ├── providers/             # AI Provider Abstraction Layer
│   │   ├── base.py            # Base abstract provider interface
│   │   ├── mock_provider.py   # Deterministic offline mock provider
│   │   ├── openai_provider.py # Official OpenAI SDK implementation
│   │   ├── gemini_provider.py # Official google-genai SDK implementation
│   │   ├── anthropic_provider.py # Official anthropic SDK implementation
│   │   └── factory.py         # Dynamic provider switching factory
│   ├── ingestion/             # Document parsers (PDF, DOCX, CSV, HTML, RSS)
│   ├── extraction/            # Civic issue extraction service
│   ├── matching/              # Hybrid deduplication & recurrence engine
│   ├── location/              # Spatial distance & jurisdiction resolver
│   ├── intelligence/          # Multi-factor explainable scoring engine
│   ├── stakeholders/          # Verified civic authority directory & mapper
│   ├── opportunities/         # Action generator & human moderation service
│   ├── prioritization/        # Weighted priority calculation engine
│   ├── workers/               # Background task queue & orchestration
│   ├── main.py                # FastAPI application entrypoint
│   └── seed.py                # Synthetic dataset seeding utility
├── data/sample/
│   └── synthetic_sources.json # 32 synthetic demonstration source records
├── docs/                      # Architectural & API documentation
│   ├── architecture.md        # Comprehensive system architecture & diagrams
│   ├── api.md                 # Complete REST API reference
│   ├── curl_examples.md       # Copy-paste cURL commands for all endpoints
│   ├── provider_configuration.md # AI Provider setup & switching guide
│   ├── frontend_integration.md # React / Next.js / TypeScript integration guide
│   └── troubleshooting_and_limitations.md # Troubleshooting & limitations
├── tests/                     # Automated pytest test suite
│   ├── conftest.py            # In-memory test database & fixtures
│   ├── test_parsers.py        # PDF, DOCX, CSV, HTML, TXT parser tests
│   ├── test_security.py       # Prompt injection & hashing tests
│   ├── test_providers.py      # Provider switching & error handling tests
│   ├── test_matching.py       # Deduplication & recurring issue tests
│   ├── test_stakeholders.py   # Authority verification tests
│   ├── test_opportunities.py  # Action generation & safety tests
│   └── test_api.py            # End-to-end API integration tests
├── .env.example               # Configuration template
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Local Docker deployment configuration
└── requirements.txt           # Python dependency specifications
```

---

## Getting Started

### 1. Requirements
- Python 3.10+ (tested on Python 3.14)
- SQLite (default zero-dependency database) or PostgreSQL

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the configuration template:
```bash
cp .env.example .env
```
Configure your active provider in `.env`:
```ini
# To run offline without API costs:
AI_PROVIDER=mock

# Or to use OpenAI:
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...

# Or to use Google Gemini:
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
GEMINI_API_KEY=...

# Or to use Anthropic Claude:
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=...
```

### 4. Seed Synthetic Demonstration Dataset
Populate the database with 32 realistic synthetic civic source records and run the full pipeline:
```bash
python -m app.seed 32
```

### 5. Start the Engine
Launch the development server using either method:
```bash
# Option A (Recommended - runner script):
python run.py

# Option B (Module runner):
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive API documentation will be available at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Running Automated Tests

Run the full automated test suite with pytest:
```bash
python -m pytest tests -v
```

All 29 tests cover:
- Multi-format document parsing (PDF, DOCX, CSV, HTML, plain text)
- Strict Pydantic schema validation
- Adversarial prompt-injection detection & input sanitization
- AI provider factory & graceful error recovery
- Hybrid deduplication & recurring issue detection
- Geographic matching with Haversine distance
- Anti-hallucination stakeholder mapping
- Volunteer action generation & safety checks
- REST API endpoints and background processing

---

## Safety, Privacy & Reliability Guarantees

1. **Prompt Injection Defense**: Untrusted text from scraped articles or user uploads is framed inside `<untrusted_source_content>` boundaries. System directives explicitly forbid the model from obeying instructions found inside raw inputs.
2. **Anti-Hallucination for Authorities**: Civic authorities are cross-referenced with a verified registry. If unverified, candidate stakeholders are explicitly labeled `CANDIDATE_UNVERIFIED` and contact numbers/emails are strictly withheld.
3. **Citizen Safety Guardrails**: Civic actions strictly forbid hazardous citizen tasks (e.g., handling live electrical wires, descending into active storm sewers, or confronting alleged offenders). Activities involving infrastructure repairs require official permits and human moderation.
4. **Human-in-the-Loop Moderation**: All generated action plans support a review lifecycle (`PENDING_REVIEW` -> `APPROVED` / `REJECTED` / `MODIFIED`) with an immutable audit trail.
