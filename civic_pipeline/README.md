# Civic Ingestion, Verification, and NGO Mobilization Pipeline

A production-ready, modular backend engine built with **Python (FastAPI)**, **Supabase (PostgreSQL + pgvector)**, and **Google Gemini (gemini-1.5-flash / text-embedding-004)** that automates the end-to-end lifecycle of civic problem signals from ingestion to volunteer citizen mobilization.

---

## 4-Step Pipeline Architecture

```
                                  [ Citizen Signals ]
                 (Tweets, Resident Grievances, News Articles, Official Notices)
                                          │
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ Step 1: Multi-Source Signal Ingestion                                       │
   │ Endpoint: POST /api/ingest/multi-source                                     │
   │ Saves raw content, source URL, and timestamp into `civic_sources`          │
   └──────────────────────────────────────┬──────────────────────────────────────┘
                                          │
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ Step 2: AI Synthesis & Authenticity Scoring (Gemini 1.5 Flash)              │
   │ Module: extractor_and_verifier.py                                           │
   │ Structured JSON Output: title, category, ward, geo-coords, severity,        │
   │ responsible authority, 0-100 credibility score, & action blueprint          │
   └──────────────────────────────────────┬──────────────────────────────────────┘
                                          │
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ Step 3: Semantic Clustering Engine (text-embedding-004 + pgvector)          │
   │ Module: clustering_engine.py                                                │
   │ Cosine distance search: `civic_issues.embedding <=> query_embedding`        │
   │ • If similarity >= 0.82 in same ward: Merge evidence, increment source     │
   │   count, and recalculate authenticity score (news corroborating social/     │
   │   resident signals grants +18 pts boost)                                    │
   │ • If similarity < 0.82: Create new issue record in `civic_issues`           │
   └──────────────────────────────────────┬──────────────────────────────────────┘
                                          │
                        Authenticity Score >= 65 (Verified)
                                          │
                                          ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ Step 4: NGO Dispatcher & Volunteer Mobilization                             │
   │ Module: ngo_dispatcher.py                                                   │
   │ • Queries registered NGOs matching issue's ward & category                  │
   │ • Pre-populates `ngo_volunteer_events` draft with gear, tasks, and safety  │
   │ • Generates real-time alert payload for NGO coordinator                     │
   └──────────────────┬───────────────────────────────────────┬──────────────────┘
                      │                                       │
                      ▼                                       ▼
   ┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
   │ NGO Actionable Feed & Publishing     │  │ Public Interactive Map Clusters   │
   │ GET  /api/ngos/{ngo_id}/feed         │  │ GET /api/public/map-clusters      │
   │ POST /api/events/publish             │  │ Pin clusters with live volunteer  │
   │ (Sets status to 'published' and      │  │ RSVPs and administrative contact  │
   │ issue to 'event_active')             │  └───────────────────────────────────┘
   └──────────────────────────────────────┘
```

---

## Database Design & SQL Migration

The complete PostgreSQL migration script is located at [`migrations/001_initial_civic_schema.sql`](file:///C:/Users/anagh/.gemini/antigravity/scratch/civic_pipeline/migrations/001_initial_civic_schema.sql).

### Tables
1. **`civic_sources`**:
   - `id` (UUID, PK)
   - `issue_id` (UUID, FK -> `civic_issues.id`)
   - `source_type` (`twitter`, `news`, `resident_complaint`, `municipal_notice`)
   - `source_url` (TEXT)
   - `raw_content` (TEXT)
   - `published_at` (TIMESTAMPTZ)
   - `status` (`raw`, `processed`, `clustered`)
2. **`civic_issues`**:
   - `id` (UUID, PK)
   - `title` (TEXT), `summary` (TEXT)
   - `category` (`Sanitation`, `Roads & Transit`, `Waterlogging`, `Public Safety`, `Environment`)
   - `ward` (VARCHAR), `latitude` (FLOAT), `longitude` (FLOAT)
   - `severity` (`Low`, `Medium`, `High`, `Critical`)
   - `authenticity_score` (INT 0-100), `verification_reasoning` (TEXT)
   - `responsible_authority` (TEXT)
   - `source_count` (INT DEFAULT 1)
   - `embedding` (VECTOR(768))
   - `status` (`flagged_unverified`, `verified_pending_ngo`, `event_active`, `resolved`)
3. **`ngos`**:
   - `id` (UUID, PK)
   - `name` (TEXT)
   - `primary_causes` (TEXT[])
   - `operating_wards` (TEXT[])
   - `contact_email` (TEXT UNIQUE)
   - `is_verified` (BOOLEAN DEFAULT TRUE)
4. **`ngo_volunteer_events`**:
   - `id` (UUID, PK)
   - `issue_id` (UUID, FK -> `civic_issues.id`)
   - `ngo_id` (UUID, FK -> `ngos.id`)
   - `event_title` (TEXT), `event_date` (DATE), `meeting_point` (TEXT)
   - `target_volunteers` (INT), `registered_volunteers` (INT DEFAULT 0)
   - `required_gear` (JSONB), `tasks_breakdown` (JSONB), `safety_guidelines` (JSONB)
   - `status` (`draft`, `published`, `completed`)

### Stored Vector Match Function
```sql
CREATE OR REPLACE FUNCTION match_similar_civic_issues (
    query_embedding VECTOR(768),
    similarity_threshold FLOAT DEFAULT 0.82,
    match_count INT DEFAULT 5,
    filter_ward VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id UUID, title TEXT, summary TEXT, category VARCHAR, ward VARCHAR,
    latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, severity VARCHAR,
    authenticity_score INT, responsible_authority TEXT, source_count INT,
    status VARCHAR, similarity FLOAT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT ci.id, ci.title, ci.summary, ci.category, ci.ward,
           ci.latitude, ci.longitude, ci.severity, ci.authenticity_score,
           ci.responsible_authority, ci.source_count, ci.status,
           (1.0 - (ci.embedding <=> query_embedding))::FLOAT AS similarity
    FROM civic_issues ci
    WHERE ci.embedding IS NOT NULL
      AND (filter_ward IS NULL OR ci.ward = filter_ward)
      AND (1.0 - (ci.embedding <=> query_embedding)) >= similarity_threshold
    ORDER BY ci.embedding <=> query_embedding ASC
    LIMIT match_count;
END;
$$;
```

---

## FastAPI REST API Endpoints

### 1. Ingest Multi-Source Signals
- **Endpoint**: `POST /api/ingest/multi-source`
- **Request Body**:
  ```json
  {
    "signals": [
      {
        "source_type": "twitter",
        "source_url": "https://x.com/resident/status/101",
        "raw_content": "Overflowing garbage dump on Koramangala Ward 151 5th Main! Stinks horribly."
      },
      {
        "source_type": "news",
        "source_url": "https://thehindu.com/news/koramangala-waste",
        "raw_content": "Reporters confirm uncollected solid waste backlog in Koramangala Ward 151."
      }
    ]
  }
  ```
- **Response**: Ingestion count, created or merged issue, similarity score, updated authenticity score, and pre-populated NGO volunteer events.

### 2. NGO Actionable Feed
- **Endpoint**: `GET /api/ngos/{ngo_id}/actionable-feed`
- **Returns**: Issues filtered by NGO's `operating_wards` and `primary_causes`, sorted by calculated priority score (`severity_weight + authenticity_score * 0.6`), including pre-populated draft mobilization cards.

### 3. Publish Volunteer Event
- **Endpoint**: `POST /api/events/publish`
- **Request Body**:
  ```json
  {
    "event_id": "d10f02af-410b-4122-bea1-0a8677bb33e5",
    "ngo_id": "c1111111-1111-4111-8111-111111111111",
    "event_title": "Operation CleanKoramangala: Citizen Trash Segregation Drive",
    "event_date": "2026-10-18",
    "meeting_point": "Koramangala 5th Main Park Entrance, Ward 151",
    "target_volunteers": 30,
    "required_gear": ["Gloves", "Heavy waste bags", "N95 masks"],
    "tasks_breakdown": ["Perimeter cordon", "Debris segregation", "Disinfection"],
    "safety_guidelines": ["Wear high-vis vests", "Do not touch glass directly"]
  }
  ```
- **Result**: Event status set to `published`, and associated issue status transitions to `event_active`.

### 4. Public Map Clusters
- **Endpoint**: `GET /api/public/map-clusters`
- **Returns**: All verified issues with active volunteer mobilization events, coordinates, meeting points, and volunteer recruitment numbers for map visualization.

---

## Quickstart & Setup

### 1. Installation
```bash
git clone <repo>
cd civic_pipeline
pip install -r requirements.txt
```

### 2. Environment Variables (`.env`)
```env
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_supabase_anon_or_service_role_key
SIMILARITY_THRESHOLD=0.82
VERIFICATION_THRESHOLD=65
HOST=0.0.0.0
PORT=8000
```

> **Note**: If `GEMINI_API_KEY` or `SUPABASE_URL` are not set, the pipeline operates in high-fidelity semantic in-memory simulation mode, allowing full local execution and testing without credentials.

### 3. Run Automated Tests
```bash
python -m pytest -v tests/test_pipeline.py
```

### 4. Run Interactive End-to-End Simulation
```bash
python scripts/seed_demo_data.py
```

### 5. Start FastAPI Development Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger docs available at `http://localhost:8000/docs`.
