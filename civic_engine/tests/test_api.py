"""Comprehensive API integration tests covering all versioned REST endpoints."""

import io


def test_api_health(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_api_config_status(client):
    res = client.get("/api/v1/config/status")
    assert res.status_code == 200
    data = res.json()
    assert data["active_provider"] == "mock"
    assert "providers_configured" in data


def test_create_and_process_source(client):
    # 1. Ingest text source
    payload = {
        "source_type": "user_text",
        "original_title": "Severe pothole on S.V. Road Andheri",
        "extracted_text": "Dangerous 8-inch crater on S.V. Road near Andheri station causing accidents.",
        "publisher": "Test Commuter",
    }
    create_res = client.post("/api/v1/sources", json=payload)
    assert create_res.status_code == 200
    source_data = create_res.json()
    source_id = source_data["id"]
    assert source_data["original_title"] == payload["original_title"]

    # 2. List sources
    list_res = client.get("/api/v1/sources")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # 3. Get source details
    detail_res = client.get(f"/api/v1/sources/{source_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["extracted_text"] == payload["extracted_text"]

    # 4. Process source synchronously
    proc_res = client.post(f"/api/v1/sources/{source_id}/process?run_async=false")
    assert proc_res.status_code == 200
    job_data = proc_res.json()
    assert job_data["status"] == "COMPLETED"

    # 5. List issues
    issues_res = client.get("/api/v1/issues")
    assert issues_res.status_code == 200
    issues = issues_res.json()["items"]
    assert len(issues) >= 1
    issue_id = issues[0]["id"]

    # 6. Get issue detail & intelligence report
    issue_detail_res = client.get(f"/api/v1/issues/{issue_id}")
    assert issue_detail_res.status_code == 200
    issue_detail = issue_detail_res.json()
    assert "Pothole" in issue_detail["title"]
    assert issue_detail["composite_priority_score"] > 0
    assert len(issue_detail["observations"]) >= 1

    # 7. Evidence endpoint
    ev_res = client.get(f"/api/v1/issues/{issue_id}/evidence")
    assert ev_res.status_code == 200
    ev_data = ev_res.json()
    assert ev_data["issue_id"] == issue_id
    assert len(ev_data["evidence_items"]) >= 1

    # 8. Stakeholders discover
    stk_disc_res = client.post(f"/api/v1/issues/{issue_id}/stakeholders/discover")
    assert stk_disc_res.status_code == 200
    stk_data = stk_disc_res.json()
    assert len(stk_data["stakeholders"]) >= 1

    # 9. List stakeholders for issue
    stk_list_res = client.get(f"/api/v1/issues/{issue_id}/stakeholders")
    assert stk_list_res.status_code == 200
    assert len(stk_list_res.json()) >= 1

    # 10. Opportunities generate
    opp_gen_res = client.post(f"/api/v1/issues/{issue_id}/opportunities/generate")
    assert opp_gen_res.status_code == 200
    opps = opp_gen_res.json()
    assert len(opps) >= 1
    opp_id = opps[0]["id"]

    # 11. List opportunities
    opp_list_res = client.get("/api/v1/opportunities")
    assert opp_list_res.status_code == 200
    assert opp_list_res.json()["total"] >= 1

    # 12. Review opportunity
    review_payload = {
        "reviewer_name": "Senior Civic Auditor",
        "status": "APPROVED",
        "feedback_comments": "Action plan verified and safe for community deployment.",
    }
    review_res = client.post(f"/api/v1/opportunities/{opp_id}/review", json=review_payload)
    assert review_res.status_code == 200
    assert review_res.json()["status"] == "APPROVED"

    # 13. Analytics endpoints
    cat_res = client.get("/api/v1/analytics/categories")
    assert cat_res.status_code == 200
    assert cat_res.json()["total_issues"] >= 1

    trend_res = client.get("/api/v1/analytics/trends")
    assert trend_res.status_code == 200

    loc_res = client.get("/api/v1/analytics/locations")
    assert loc_res.status_code == 200

    opp_stat_res = client.get("/api/v1/analytics/opportunities")
    assert opp_stat_res.status_code == 200
    assert opp_stat_res.json()["total_opportunities"] >= 1


def test_file_upload_api(client):
    file_content = b"Complaint ID,Locality,Issue\n1,Milan Subway,Choked storm water drain causes flooding"
    files = {"file": ("test_complaints.csv", io.BytesIO(file_content), "text/csv")}
    res = client.post("/api/v1/sources/upload", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["source_type"] == "csv"
    assert data["original_title"] == "test_complaints.csv"
