# Quickstart cURL Command Reference

Make sure the backend server is running on `http://127.0.0.1:8000`:
```bash
python run.py
# or:
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 1. System Health & Configuration

### Check Health
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/health"
```

### Check Active Provider & Safe Config
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/config/status"
```

---

## 2. Ingesting Sources

### Ingest Direct Text Complaint
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sources" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "user_text",
    "original_title": "Severe Pothole on S.V. Road near Station",
    "extracted_text": "An 8-inch deep crater on S.V. Road Andheri West has developed, creating two-wheeler hazards and heavy traffic snarls.",
    "publisher": "Citizen Commuter"
  }'
```

### Ingest Public URL
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sources" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "news_web",
    "original_title": "Local News Article",
    "original_url": "https://example.com/article",
    "publisher": "City Times"
  }'
```

### Upload Evidentiary Document (PDF / CSV / DOCX)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sources/upload" \
  -F "file=@./test_complaints.csv" \
  -F "publisher=Ward Citizen Cell"
```

### Process Source Synchronously
*(Replace `{source_id}` with an actual ID from ingestion)*
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sources/{source_id}/process?run_async=false"
```

---

## 3. Civic Issues & Intelligence

### List Top Prioritized Issues
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/issues?page=1&page_size=10"
```

### Filter Recurring Chronic Issues
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/issues?is_recurring=true"
```

### Retrieve Issue Details & Intelligence Report
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/issues/{issue_id}"
```

### Find Related & Recurring Issues Across City
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/issues/{issue_id}/find-related"
```

### Get Full Evidentiary Dossier & Provenance Citations
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/issues/{issue_id}/evidence"
```

---

## 4. Stakeholder Discovery

### Discover Responsible Civic Authorities & Ward Offices
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/issues/{issue_id}/stakeholders/discover"
```

### List Mapped Stakeholders for Issue
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/issues/{issue_id}/stakeholders"
```

---

## 5. Civic Opportunities & Actions

### Generate Practical Citizen Action Opportunities
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/issues/{issue_id}/opportunities/generate"
```

### List Volunteer Opportunities Sorted by Priority
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/opportunities"
```

### Review & Moderate Opportunity
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/opportunities/{opportunity_id}/review" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_name": "Senior Civic Coordinator",
    "status": "APPROVED",
    "feedback_comments": "Verified protocol adheres to public pedestrian safety guidelines."
  }'
```

---

## 6. Real-Time Analytics

### Category Volume & Priority Breakdown
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/analytics/categories"
```

### Temporal Recurrence & Trends
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/analytics/trends"
```

### Geographic Hotspots & Ward Distribution
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/analytics/locations"
```

### Volunteer Opportunity Metrics
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/analytics/opportunities"
```
