# REST API Reference - Version 1 (`/api/v1`)

The Civic Issue Discovery & Action Engine provides versioned REST API endpoints adhering to standard HTTP conventions and returning JSON responses.

Interactive Swagger documentation is available at `/docs` and ReDoc at `/redoc`.

---

## 1. Health & Configuration

### `GET /api/v1/health`
Checks whether the service is running.
- **Response `200 OK`**:
```json
{
  "status": "ok",
  "service": "Civic Issue Discovery & Action Engine",
  "version": "1.0.0",
  "timestamp": "2026-10-11T12:00:00Z"
}
```

### `GET /api/v1/config/status`
Returns safe, non-sensitive configuration parameters. Secret API keys are never exposed.
- **Response `200 OK`**:
```json
{
  "project_name": "Civic Issue Discovery & Action Engine",
  "version": "1.0.0",
  "active_provider": "openai",
  "active_model": "gpt-4o-mini",
  "providers_configured": {
    "mock": true,
    "openai": true,
    "gemini": false,
    "anthropic": false
  },
  "database_type": "sqlite",
  "request_timeout_seconds": 30,
  "max_retries": 3,
  "api_auth_enabled": false,
  "discovery_enabled": true,
  "discovery_interval_minutes": 60
}
```

### `GET /api/v1/jobs/{job_id}`
Inspects the execution status of an asynchronous background job.
- **Response `200 OK`**:
```json
{
  "id": "c1f7b029-4a9c-4861-a589-9a25b16955a9",
  "job_type": "FULL_PIPELINE",
  "status": "COMPLETED",
  "source_id": "82f1b4c0-43f1-46ee-8df3-376c66cf1eb3",
  "progress_percentage": 100,
  "total_items": 1,
  "processed_items": 1,
  "result_summary": {
    "observations_extracted": 1,
    "consolidated_issues_count": 1,
    "stakeholders_mapped": 2,
    "opportunities_created": 1
  },
  "created_at": "2026-10-11T12:05:00Z",
  "completed_at": "2026-10-11T12:05:03Z"
}
```

---

## 2. Sources

### `POST /api/v1/sources`
Ingest raw text or public URL.
- **Request Body**:
```json
{
  "source_type": "user_text",
  "original_title": "Severe Potholes on S.V. Road near Andheri station",
  "extracted_text": "Craters extending up to 8 inches deep have disrupted traffic...",
  "publisher": "Local Commuter Association"
}
```
- **Response `200 OK`**: Returns normalized `SourceResponse` with SHA-256 hash.

### `POST /api/v1/sources/upload`
Upload an evidentiary file (`multipart/form-data`). Supported formats: `.pdf`, `.docx`, `.csv`, `.txt`, `.md`. Maximum 10MB.
- **Form Fields**: `file` (binary), `publisher` (string, optional)
- **Response `200 OK`**: Returns normalized `SourceResponse`.

### `GET /api/v1/sources`
List ingested sources with pagination and filtering.
- **Query Params**:
  - `source_type`: Filter by source type (`rss`, `news_web`, `pdf`, `user_text`, etc.)
  - `status`: Filter by processing status (`PENDING`, `COMPLETED`, `FAILED`, `DUPLICATE`)
  - `page`: Page index (default `1`)
  - `page_size`: Items per page (default `20`, max `100`)

### `GET /api/v1/sources/{source_id}`
Returns complete source record including full text, metadata payload, and linked observations count.

### `POST /api/v1/sources/{source_id}/process`
Trigger AI processing on a source.
- **Query Params**: `run_async` (`true` to return background job ID, `false` to block until completed).

---

## 3. Civic Issues & Intelligence

### `POST /api/v1/discovery/run`
Trigger proactive discovery loop across all pending sources.

### `POST /api/v1/issues/analyze`
Run batch clustering, deduplication, and multi-factor intelligence scoring on all unassigned observations.

### `GET /api/v1/issues`
List consolidated civic issues.
- **Query Params**:
  - `category`: Filter by civic category
  - `is_recurring`: `true` or `false`
  - `min_priority`: Float between `0.0` and `100.0`
  - `search`: Keyword search in title, location, and summary
  - `page`: Page number
  - `page_size`: Page size

### `GET /api/v1/issues/{issue_id}`
Retrieve complete intelligence dossier for an issue, including multi-factor score breakdown, what/where analysis, missing info, and linked individual observations.

### `POST /api/v1/issues/{issue_id}/find-related`
Identify and score cross-issue relationships (`DUPLICATE_REPORT`, `RECURRING_INCIDENT`, `NEARBY_SIMILAR`, `CROSS_AREA_SIMILAR`, `UNRELATED_KEYWORD_MATCH`) with transparent reasons.

### `GET /api/v1/issues/{issue_id}/evidence`
Retrieve evidentiary dossier containing all verbatim quotes, original source publications, and corroboration metrics.

---

## 4. Stakeholders

### `GET /api/v1/issues/{issue_id}/stakeholders`
List statutory authorities, municipal departments, and civic NGOs mapped to an issue.

### `POST /api/v1/issues/{issue_id}/stakeholders/discover`
Trigger statutory authority discovery combining verified municipal registries and contextual AI recommendations.

---

## 5. Civic Opportunities

### `POST /api/v1/issues/{issue_id}/opportunities/generate`
Generate practical, safe citizen action opportunities and volunteer tasks.

### `GET /api/v1/opportunities`
List civic opportunities sorted by priority score.
- **Query Params**:
  - `review_status`: `PENDING_REVIEW`, `APPROVED`, `REJECTED`, `MODIFIED`
  - `activity_type`: `EVIDENCE_COLLECTION`, `COMMUNITY_SURVEY`, `OFFICIAL_GRIEVANCE_FILING`, etc.
  - `safety_risk_level`: `LOW`, `MODERATE`, `HIGH_REQUIRES_AUTHORITY`

### `GET /api/v1/opportunities/{opportunity_id}`
Fetch full opportunity action plan, volunteer roles, safety requirements, and expected outcomes.

### `POST /api/v1/opportunities/{opportunity_id}/review`
Submit human moderation review:
- **Request Body**:
```json
{
  "reviewer_name": "Civic Moderator",
  "status": "APPROVED",
  "feedback_comments": "Verified protocol adheres to public safety guidelines."
}
```

---

## 6. Analytics

- `GET /api/v1/analytics/categories`: Issue volume and average priority across categories.
- `GET /api/v1/analytics/trends`: Temporal trend patterns (chronic, escalating, stable, new).
- `GET /api/v1/analytics/locations`: Geographic hot spots, wards, and coordinates.
- `GET /api/v1/analytics/opportunities`: Metrics on opportunities, review statuses, and volunteer hours.
