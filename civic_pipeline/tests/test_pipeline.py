import unittest
from datetime import datetime, date, timezone
from uuid import UUID, uuid4
from fastapi.testclient import TestClient

from app.main import app
from app.database import reset_repository_for_testing, get_repository
from app.models.schemas import (
    SourceType,
    CivicCategory,
    SeverityLevel,
    IssueStatus,
    EventStatus,
    RawSignalInput,
    MultiSourceIngestRequest,
    CivicVerificationResult,
    Coordinates,
    SuggestedActionBlueprint,
)
from app.ai.clustering_engine import get_clustering_engine
from app.ai.extractor_and_verifier import get_extractor_and_verifier
from app.ai.ngo_dispatcher import get_ngo_dispatcher


class TestCivicPipeline(unittest.TestCase):
    def setUp(self):
        # Reset state before each test
        self.repo = reset_repository_for_testing()
        self.client = TestClient(app)
        self.clustering_engine = get_clustering_engine()
        self.clustering_engine.repo = self.repo
        self.extractor = get_extractor_and_verifier()
        self.dispatcher = get_ngo_dispatcher()
        self.dispatcher.repo = self.repo

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("similarity_threshold", data)
        self.assertEqual(data["similarity_threshold"], 0.82)
        self.assertEqual(data["verification_threshold"], 65)

    def test_pydantic_schemas_validation(self):
        coord = Coordinates(latitude=12.9352, longitude=77.6245)
        self.assertAlmostEqual(coord.latitude, 12.9352)

        blueprint = SuggestedActionBlueprint(
            event_title="Community Sanitation Drive",
            required_gear=["Gloves", "Bags"],
            tasks_breakdown=["Collect debris", "Bag trash"],
            safety_guidelines=["Avoid sharp objects"]
        )
        self.assertEqual(len(blueprint.required_gear), 2)

        result = CivicVerificationResult(
            title="Massive Garbage Pile",
            summary="Garbage dumped near 5th Block junction",
            category=CivicCategory.SANITATION,
            ward="Koramangala Ward 151",
            coordinates=coord,
            severity=SeverityLevel.HIGH,
            responsible_authority="BBMP Solid Waste Management",
            authenticity_score=78,
            authenticity_breakdown="Multiple corroborating reports with specific street landmark",
            suggested_action_blueprint=blueprint
        )
        self.assertEqual(result.authenticity_score, 78)
        self.assertEqual(result.severity, SeverityLevel.HIGH)

    def test_ai_extraction_and_verification(self):
        signals = [
            RawSignalInput(
                source_type=SourceType.TWITTER,
                source_url="https://x.com/resident/status/101",
                raw_content="Terrible garbage dump overflowing at Koramangala Ward 151 5th Main near the junction! Stinking for 3 days.",
                published_at=datetime.now(timezone.utc)
            )
        ]
        verification = self.extractor.process_raw_signals(signals)
        self.assertEqual(verification.category, CivicCategory.SANITATION)
        self.assertIn("Koramangala", verification.ward)
        self.assertGreaterEqual(verification.authenticity_score, 50)
        self.assertTrue(len(verification.suggested_action_blueprint.required_gear) > 0)
        self.assertTrue(len(verification.suggested_action_blueprint.tasks_breakdown) > 0)

    def test_clustering_new_issue_creation(self):
        payload = {
            "signals": [
                {
                    "source_type": "resident_complaint",
                    "source_url": "https://civic-portal.gov.in/tickets/8821",
                    "raw_content": "Deep crater and pothole near Koramangala Ward 151 80 Feet Road junction. Two bikers skidded this morning.",
                    "published_at": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        response = self.client.post("/api/ingest/multi-source", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()

        self.assertEqual(data["ingested_source_count"], 1)
        self.assertEqual(data["cluster_action"], "created_new_issue")
        self.assertIn("Roads & Transit", data["issue"]["category"])
        self.assertIn("Koramangala", data["issue"]["ward"])
        self.assertEqual(data["issue"]["source_count"], 1)

    def test_clustering_corroboration_merge_and_authenticity_boost(self):
        # Step 1: Ingest social media report about waterlogging in HSR Layout Ward 174
        signal_1 = {
            "signals": [
                {
                    "source_type": "twitter",
                    "source_url": "https://x.com/hsr_comm/status/201",
                    "raw_content": "Severe waterlogging and submerged street near HSR Layout Ward 174 27th Main drain canal overflow!",
                    "published_at": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        res1 = self.client.post("/api/ingest/multi-source", json=signal_1)
        self.assertEqual(res1.status_code, 201)
        data1 = res1.json()
        initial_issue_id = data1["issue"]["id"]
        initial_score = data1["authenticity_score"]

        # Step 2: Ingest corroborating e-news article for the exact same location and problem
        signal_2 = {
            "signals": [
                {
                    "source_type": "news",
                    "source_url": "https://deccanherald.com/city/hsr-drain-flood",
                    "raw_content": "Reporters confirm heavy monsoon waterlogging and submerged streets at HSR Layout Ward 174 27th Main drain canal.",
                    "published_at": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        res2 = self.client.post("/api/ingest/multi-source", json=signal_2)
        self.assertEqual(res2.status_code, 201)
        data2 = res2.json()

        # Step 3: Verify clustering merged into the existing issue
        self.assertEqual(data2["cluster_action"], "merged_existing_cluster")
        self.assertEqual(data2["issue"]["id"], initial_issue_id)
        self.assertEqual(data2["issue"]["source_count"], 2)
        self.assertIsNotNone(data2["similarity_score"])
        self.assertGreaterEqual(data2["similarity_score"], 0.82)

        # Step 4: Verify authenticity score increased when independent news corroborated social media
        merged_score = data2["authenticity_score"]
        self.assertGreater(merged_score, initial_score)
        self.assertIn("corroborat", data2["issue"]["verification_reasoning"].lower())

    def test_ngo_dispatcher_and_actionable_feed(self):
        # Ingest a high-credibility sanitation signal in Koramangala Ward 151
        payload = {
            "signals": [
                {
                    "source_type": "news",
                    "source_url": "https://timesofindia.com/city/koramangala-waste",
                    "raw_content": "Official municipal sanitation crisis: News reporters and multiple residents confirm large illegal garbage dump at Koramangala Ward 151 5th Main.",
                    "published_at": datetime.now(timezone.utc).isoformat()
                },
                {
                    "source_type": "resident_complaint",
                    "source_url": "https://bbmp.gov.in/c/992",
                    "raw_content": "Multiple residents filed formal complaints regarding the Koramangala Ward 151 5th Main sanitation dump.",
                    "published_at": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        res = self.client.post("/api/ingest/multi-source", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()

        # Check authenticity score is >= 65 and drafts were created
        self.assertGreaterEqual(data["authenticity_score"], 65)
        self.assertTrue(len(data["dispatched_events"]) > 0)
        self.assertTrue(len(data["ngo_alerts"]) > 0)

        ngo_id = data["dispatched_events"][0]["ngo_id"]

        # Query GET /api/ngos/{ngo_id}/actionable-feed
        feed_res = self.client.get(f"/api/ngos/{ngo_id}/actionable-feed")
        self.assertEqual(feed_res.status_code, 200)
        feed_items = feed_res.json()

        self.assertGreaterEqual(len(feed_items), 1)
        first_item = feed_items[0]
        self.assertEqual(first_item["issue"]["ward"], "Koramangala Ward 151")
        self.assertEqual(first_item["issue"]["category"], "Sanitation")
        self.assertIsNotNone(first_item["event_draft"])
        self.assertEqual(first_item["event_draft"]["status"], "draft")
        self.assertGreater(first_item["recommended_priority_score"], 50.0)

    def test_publish_volunteer_event_and_public_map(self):
        # 1. Ingest verified road problem in Koramangala Ward 151
        # Matching NGO: c2222222-2222-4222-8222-222222222222 (SafeRoads & Rapid Drainage Collective)
        payload = {
            "signals": [
                {
                    "source_type": "news",
                    "source_url": "https://thehindu.com/news/koramangala-road",
                    "raw_content": "Times of India reporters and official ward engineers confirm hazardous road transit crater at Koramangala Ward 151 main junction.",
                    "published_at": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        ingest_res = self.client.post("/api/ingest/multi-source", json=payload)
        self.assertEqual(ingest_res.status_code, 201)
        ingest_data = ingest_res.json()

        self.assertTrue(len(ingest_data["dispatched_events"]) > 0)
        event_draft = ingest_data["dispatched_events"][0]
        event_id = event_draft["id"]
        ngo_id = event_draft["ngo_id"]
        issue_id = event_draft["issue_id"]

        # 2. NGO reviews and publishes event via POST /api/events/publish
        publish_payload = {
            "event_id": event_id,
            "ngo_id": ngo_id,
            "event_title": "Koramangala Pothole Patch & Citizen Road Safety Drive",
            "event_date": "2026-10-18",
            "meeting_point": "Opposite Koramangala Club Main Gate",
            "target_volunteers": 25,
            "required_gear": ["High-vis vests", "Cold mix asphalt", "Tamping tool", "Gloves"],
            "tasks_breakdown": ["Traffic cordoning", "Crater debris cleanup", "Asphalt leveling", "Tamping"],
            "safety_guidelines": ["Stay behind traffic cones", "Wear high-vis vests at all times"]
        }
        pub_res = self.client.post("/api/events/publish", json=publish_payload)
        self.assertEqual(pub_res.status_code, 200)
        pub_data = pub_res.json()

        self.assertEqual(pub_data["status"], "published")
        self.assertEqual(pub_data["event_title"], "Koramangala Pothole Patch & Citizen Road Safety Drive")
        self.assertEqual(pub_data["target_volunteers"], 25)

        # 3. Verify the associated civic issue has updated status to 'event_active'
        issue_record = self.repo.get_issue(issue_id)
        self.assertEqual(issue_record["status"], IssueStatus.EVENT_ACTIVE.value)

        # 4. Verify public map clusters via GET /api/public/map-clusters
        map_res = self.client.get("/api/public/map-clusters")
        self.assertEqual(map_res.status_code, 200)
        clusters = map_res.json()

        self.assertGreaterEqual(len(clusters), 1)
        matched_cluster = next((c for c in clusters if c["issue_id"] == issue_id), None)
        self.assertIsNotNone(matched_cluster)
        self.assertEqual(matched_cluster["status"], "event_active")
        self.assertEqual(len(matched_cluster["active_events"]), 1)
        active_event = matched_cluster["active_events"][0]
        self.assertEqual(active_event["event_title"], "Koramangala Pothole Patch & Citizen Road Safety Drive")
        self.assertEqual(active_event["status"], "published")
        self.assertEqual(active_event["target_volunteers"], 25)

    def test_edge_cases_and_error_handling(self):
        # 1. Empty signals list triggers 422 Unprocessable Entity (min_length=1)
        res_empty = self.client.post("/api/ingest/multi-source", json={"signals": []})
        self.assertEqual(res_empty.status_code, 422)

        # 2. Non-existent NGO feed returns 404
        fake_ngo_id = str(uuid4())
        res_fake_ngo = self.client.get(f"/api/ngos/{fake_ngo_id}/actionable-feed")
        self.assertEqual(res_fake_ngo.status_code, 404)

        # 3. Publish non-existent event returns 404
        fake_event_id = str(uuid4())
        valid_ngo_id = "c1111111-1111-4111-8111-111111111111"
        res_fake_event = self.client.post("/api/events/publish", json={
            "event_id": fake_event_id,
            "ngo_id": valid_ngo_id,
            "event_title": "Fake Event"
        })
        self.assertEqual(res_fake_event.status_code, 404)

        # 4. Ingest issue and try publishing with WRONG NGO id -> 403 Forbidden
        ingest_res = self.client.post("/api/ingest/multi-source", json={
            "signals": [{
                "source_type": "news",
                "raw_content": "Official municipal notice: Urgent tree fall hazard blocking Koramangala Ward 151 4th Block road.",
                "published_at": datetime.now(timezone.utc).isoformat()
            }]
        })
        self.assertEqual(ingest_res.status_code, 201)
        data = ingest_res.json()
        if data["dispatched_events"]:
            real_event = data["dispatched_events"][0]
            unauthorized_ngo_id = "c3333333-3333-4333-8333-333333333333"
            res_forbidden = self.client.post("/api/events/publish", json={
                "event_id": real_event["id"],
                "ngo_id": unauthorized_ngo_id,
                "event_title": "Hacked Event"
            })
            self.assertEqual(res_forbidden.status_code, 403)


if __name__ == "__main__":
    unittest.main()

