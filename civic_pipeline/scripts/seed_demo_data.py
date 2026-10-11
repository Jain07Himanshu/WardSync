"""
End-to-end simulation demonstration for the
Civic Ingestion, Verification, and NGO Mobilization Pipeline.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_repository


def run_demonstration():
    print("=" * 80)
    print("CIVIC INGESTION, VERIFICATION, AND NGO MOBILIZATION PIPELINE")
    print("End-to-End System Demonstration")
    print("=" * 80)

    client = TestClient(app)
    repo = get_repository()

    # Step 0: Check Health
    health = client.get("/health").json()
    print(f"\n[Step 0] Health Check: {health['status']}")
    print(f"         Similarity Threshold: {health['similarity_threshold']}")
    print(f"         Verification Threshold: {health['verification_threshold']}")

    # Step 1: Ingest Initial Social Media & Resident Complaint Signals
    print("\n" + "-" * 80)
    print("[Step 1] Ingesting initial social media tweet & citizen complaint...")
    print("-" * 80)

    batch_1 = {
        "signals": [
            {
                "source_type": "twitter",
                "source_url": "https://x.com/koramangala_civic/status/19827391",
                "raw_content": "Massive illegal garbage dump overflowing on Koramangala Ward 151 5th Main Rd! Stray cattle eating plastic, stinks horribly.",
                "published_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "source_type": "resident_complaint",
                "source_url": "https://bbmp.sahaaya.in/grievance/77192",
                "raw_content": "Garbage contractor has not cleared waste bin at Koramangala Ward 151 5th Main near the junction for 4 days.",
                "published_at": datetime.now(timezone.utc).isoformat()
            }
        ]
    }

    res1 = client.post("/api/ingest/multi-source", json=batch_1)
    if res1.status_code != 201:
        print(f"Ingestion failed: {res1.text}")
        return
    out1 = res1.json()

    issue_id = out1["issue"]["id"]
    print(f">> Cluster Action:       {out1['cluster_action']}")
    print(f">> Issue ID:             {issue_id}")
    print(f">> Title:                {out1['issue']['title']}")
    print(f">> Category:             {out1['issue']['category']}")
    print(f">> Ward:                 {out1['issue']['ward']}")
    print(f">> Severity:             {out1['issue']['severity']}")
    print(f">> Authenticity Score:   {out1['authenticity_score']}/100")
    print(f">> Responsible Dept:     {out1['issue']['responsible_authority']}")
    print(f">> Sources Ingested:     {out1['ingested_source_count']}")

    # Step 2: Corroborating Signal (Independent News Article)
    print("\n" + "-" * 80)
    print("[Step 2] Ingesting corroborating investigative news article...")
    print("-" * 80)

    batch_2 = {
        "signals": [
            {
                "source_type": "news",
                "source_url": "https://thehindu.com/news/cities/bangalore/koramangala-waste-crisis",
                "raw_content": "Journalists investigate sanitation failure at Koramangala Ward 151 5th Main: BBMP solid waste loaders fail to collect overflowing trash for over 96 hours.",
                "published_at": datetime.now(timezone.utc).isoformat()
            }
        ]
    }

    res2 = client.post("/api/ingest/multi-source", json=batch_2)
    out2 = res2.json()

    print(f">> Cluster Action:       {out2['cluster_action']}")
    print(f">> Vector Similarity:    {out2['similarity_score']:.4f} (Threshold: 0.82)")
    print(f">> Issue ID:             {out2['issue']['id']} (Identical to initial issue: {out2['issue']['id'] == issue_id})")
    print(f">> Updated Source Count: {out2['issue']['source_count']}")
    print(f">> Boosted Authenticity: {out2['authenticity_score']}/100 (Up from {out1['authenticity_score']}/100)")
    print(f">> Reasoning:            {out2['issue']['verification_reasoning']}")

    # Step 3: NGO Dispatcher Verification & Actionable Feed
    print("\n" + "-" * 80)
    print("[Step 3] Querying NGO Actionable Feed...")
    print("-" * 80)

    # CleanCity Green Action Foundation is registered for Koramangala Ward 151 & Sanitation
    ngo_id = "c1111111-1111-4111-8111-111111111111"
    feed_res = client.get(f"/api/ngos/{ngo_id}/actionable-feed")
    feed = feed_res.json()

    print(f"NGO Feed Items Found: {len(feed)}")
    if not feed:
        print("No items in feed!")
        return

    top_item = feed[0]
    draft_event = top_item.get("event_draft")
    print(f">> Recommended Priority: {top_item['recommended_priority_score']}")
    print(f">> Issue:                {top_item['issue']['title']}")
    print(f">> Pre-populated Draft:  {draft_event['event_title'] if draft_event else 'None'}")
    print(f">> Draft Event ID:       {draft_event['id']}")
    print(f">> Suggested Headcount:  {draft_event['target_volunteers']} volunteers")
    print(f">> Required Gear:        {draft_event['required_gear']}")
    print(f">> Tasks Breakdown:      {draft_event['tasks_breakdown']}")

    # Step 4: NGO Customizes & Publishes Volunteer Mobilization Event
    print("\n" + "-" * 80)
    print("[Step 4] NGO Accepts & Publishes Event Live for Citizen Recruitment...")
    print("-" * 80)

    event_id = draft_event["id"]
    publish_req = {
        "event_id": event_id,
        "ngo_id": ngo_id,
        "event_title": "Operation CleanKoramangala: Citizen Trash Segregation & Alleyway Clearance",
        "event_date": "2026-10-18",
        "meeting_point": "Koramangala 5th Main Park Entrance, Ward 151",
        "target_volunteers": 30,
        "required_gear": [
            "Puncture-resistant work gloves",
            "Color-coded heavy duty waste sacks",
            "Safety masks (N95)",
            "Trash grabbers and rakes"
        ],
        "tasks_breakdown": [
            "08:30 AM: Volunteer check-in & safety orientation",
            "09:00 AM: Cordon perimeter and separate recyclables from organic compost",
            "10:30 AM: Load waste onto municipal compactor truck",
            "11:15 AM: Disinfect sidewalk with lime powder"
        ],
        "safety_guidelines": [
            "Do not touch hazardous or glass items directly",
            "Wear supplied high-visibility vests",
            "Hydration points set up at tent station"
        ]
    }

    pub_res = client.post("/api/events/publish", json=publish_req)
    pub_data = pub_res.json()

    print(f">> Published Event Title: {pub_data['event_title']}")
    print(f">> Status:                {pub_data['status']}")
    print(f">> Scheduled Date:        {pub_data['event_date']}")
    print(f">> Meeting Location:      {pub_data['meeting_point']}")
    print(f">> Target Headcount:      {pub_data['target_volunteers']} citizens")

    # Step 5: Public Citizen Map Visualization
    print("\n" + "-" * 80)
    print("[Step 5] Public Map Rendering (GET /api/public/map-clusters)...")
    print("-" * 80)

    map_res = client.get("/api/public/map-clusters")
    clusters = map_res.json()

    print(f"Active Map Clusters: {len(clusters)}")
    for cluster in clusters:
        print(f"\n[Map Pin] {cluster['title']}")
        print(f"          Ward: {cluster['ward']} | Geo: ({cluster['latitude']}, {cluster['longitude']})")
        print(f"          Severity: {cluster['severity']} | Authenticity: {cluster['authenticity_score']}/100")
        print(f"          Responsible Authority: {cluster['responsible_authority']}")
        print(f"          Active Mobilization Events: {len(cluster['active_events'])}")
        for ev in cluster["active_events"]:
            print(f"          * [{ev['status'].upper()}] {ev['event_title']}")
            print(f"            Host NGO: {ev['ngo_name']}")
            print(f"            Date: {ev['event_date']} | Meeting: {ev['meeting_point']}")
            print(f"            Recruiting: {ev['registered_volunteers']}/{ev['target_volunteers']} volunteers")

    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_demonstration()
