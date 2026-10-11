"""Integration verification script for WardSync unified server and Mumbai-Thane civic dataset."""

from fastapi.testclient import TestClient
from unified_server import app

REQUIRED_22_FIELDS = [
    "report_id",
    "resident_id",
    "issue_type",
    "issue_description",
    "issue_status",
    "report_datetime",
    "location_street_address",
    "location_city",
    "location_state",
    "location_postal_code",
    "location_country",
    "latitude",
    "longitude",
    "municipal_department",
    "resolution_datetime",
    "is_anonymous",
    "priority_level",
    "priority_score",
    "severity_score",
    "area_importance",
    "citizen_reports_count",
    "resolution_days",
]

with TestClient(app) as client:
    print("=" * 80)
    print("TESTING WARDSYNC UNIFIED SERVER INTEGRATION & MUMBAI-THANE DATASET")
    print("=" * 80)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    print("1. Health Check:", data["status"])
    print("   Subsystems:", list(data["subsystems"].keys()))

    # 2. Get live frontend issues
    res = client.get("/api/public/issues")
    assert res.status_code == 200
    issues = res.json()
    print(f"2. Frontend Issues Retrieved: {len(issues)} issues")
    assert len(issues) >= 15, f"Expected >= 15 issues, got {len(issues)}"
    first_issue = issues[0]
    print(f"   First Issue: '{first_issue['title']}' at {first_issue['locality']} ({first_issue['ward']})")
    assert any(iss["locality"] == "Dadar" for iss in issues)
    assert any(iss["locality"] == "Majiwada" for iss in issues)

    # 3. Test raw dataset endpoint (JSON) with 22 required fields
    res = client.get("/api/dataset/mumbai-thane")
    assert res.status_code == 200
    raw_dataset = res.json()
    print(f"3. Raw Dataset JSON: {len(raw_dataset)} records")
    assert len(raw_dataset) == 15
    for idx, record in enumerate(raw_dataset):
        for field in REQUIRED_22_FIELDS:
            assert field in record, f"Field '{field}' missing in record {idx}"
    print(f"   Verified all 22 required fields present in all 15 records!")
    print(f"   Sample Record ID: {raw_dataset[0]['report_id']}, City: {raw_dataset[0]['location_city']}")

    # 4. Test raw dataset CSV download endpoint
    res = client.get("/api/dataset/mumbai-thane/csv")
    assert res.status_code == 200
    assert "text/csv" in res.headers.get("content-type", "")
    csv_text = res.text
    header_line = csv_text.splitlines()[0]
    for field in REQUIRED_22_FIELDS:
        assert field in header_line, f"Field '{field}' missing from CSV header"
    print("4. Raw Dataset CSV: Successfully downloaded with all 22 header columns!")

    # 5. Citizen reports issue in Mumbai (Dadar West)
    report_mumbai = {
        "title": "Severe road crater outside Dadar Flower Market",
        "category": "Roads & Transport",
        "ward": "Ward G/North (Dadar)",
        "locality": "Dadar West",
        "description": "Deep asphalt crater causing traffic gridlock and two-wheeler skids on Senapati Bapat Marg.",
        "severity": "Critical",
        "evidenceNote": "Live photos showing exposed underground utility duct.",
        "latitude": 19.0185,
        "longitude": 72.8425
    }
    res = client.post("/api/public/issues", json=report_mumbai)
    assert res.status_code == 201
    new_mum_issue = res.json()
    print(f"5. Reported Mumbai Issue: '{new_mum_issue['title']}' (ID: {new_mum_issue['id']})")
    print(f"   Authority: {new_mum_issue['responsibleAuthority']['name']}")
    assert "Brihanmumbai Municipal Corporation" in new_mum_issue['responsibleAuthority']['name']
    assert new_mum_issue['evidenceConfidence'] == 68

    # 6. Citizen reports issue in Thane (Majiwada)
    report_thane = {
        "title": "Flooded service road under Majiwada flyover",
        "category": "Water & Sanitation",
        "ward": "Ward 3 (Majiwada, Thane)",
        "locality": "Majiwada",
        "description": "Overflown stormwater gutter submerging pedestrian zebra crossing.",
        "severity": "High",
        "evidenceNote": "Video submitted by local resident.",
        "latitude": 19.2190,
        "longitude": 72.9785
    }
    res = client.post("/api/public/issues", json=report_thane)
    assert res.status_code == 201
    new_tha_issue = res.json()
    print(f"6. Reported Thane Issue: '{new_tha_issue['title']}' (ID: {new_tha_issue['id']})")
    print(f"   Authority: {new_tha_issue['responsibleAuthority']['name']}")
    assert "Thane Municipal Corporation" in new_tha_issue['responsibleAuthority']['name']

    # 7. Ingest multi-source signals into civic_pipeline
    signal_payload = {
        "signals": [
            {
                "source_type": "twitter",
                "source_url": "https://x.com/mumbaicitizen/98213",
                "raw_content": "Dangerous open culvert on SV Road Bandra West near Talao! BMC please fix.",
                "published_at": "2026-10-11T12:00:00Z"
            }
        ]
    }
    res = client.post("/api/ingest/multi-source", json=signal_payload)
    assert res.status_code == 201
    pipeline_result = res.json()
    print(f"7. Multi-Source Signal Ingested: Cluster Action={pipeline_result['cluster_action']}, Issue ID={pipeline_result['issue']['id']}")

    # 8. Citizen records donation
    res = client.post("/api/donations", json={
        "issueId": new_mum_issue["id"],
        "amount": 7500,
        "donorName": "Aarav Patil",
        "isAnonymous": False
    })
    assert res.status_code == 200
    print(f"8. Citizen Donation Recorded: Total Raised=INR {res.json()['totalRaised']}")

    # 9. Government official updates status
    res = client.patch(f"/api/issues/{new_mum_issue['id']}/status", json={"status": "In progress"})
    assert res.status_code == 200
    print(f"9. Issue Status Updated: {res.json()['newStatus']}")

    # 10. Civic Engine SQLite consolidated issues & categories
    res = client.get("/api/v1/issues")
    assert res.status_code == 200
    engine_issues = res.json()
    print(f"10. Civic Engine Consolidated Issues: Count={engine_issues['total']}")
    assert engine_issues['total'] >= 15

    res = client.get("/api/v1/analytics/categories")
    assert res.status_code == 200
    categories = res.json()
    print(f"    Civic Engine Analytics Categories: {len(categories['categories'])} categories tracked")

    print("\n" + "=" * 80)
    print("ALL INTEGRATION & DATASET TESTS PASSED 100%!")
    print("=" * 80)
