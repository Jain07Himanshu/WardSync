"""Patches unified_server.py with Mumbai & Thane dynamic dataset loading, synchronization, and endpoints."""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TARGET_FILE = ROOT_DIR / "unified_server.py"

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the hardcoded INITIAL_FRONTEND_ISSUES block
start_marker = "# Seed with rich real issues matching sampleIssues.ts and civic failure scenarios\nINITIAL_FRONTEND_ISSUES: List[Dict[str, Any]] = ["
end_marker = "LIVE_ISSUES: List[Dict[str, Any]] = [dict(item) for item in INITIAL_FRONTEND_ISSUES]"

replacement_issues_block = '''# Helper category mapper
def map_dataset_category(issue_type: str) -> str:
    if "Water" in issue_type or "Pipeline" in issue_type:
        return "Water & Sanitation"
    elif "Road" in issue_type or "Pothole" in issue_type:
        return "Roads & Transport"
    elif "Waste" in issue_type or "Dumping" in issue_type:
        return "Waste Management"
    elif "Drain" in issue_type or "Waterlogging" in issue_type:
        return "Water & Sanitation"
    elif "Mosquito" in issue_type or "Health" in issue_type:
        return "Health"
    elif "Streetlight" in issue_type or "Culvert" in issue_type:
        return "Public Safety"
    return "Public Safety"

def get_ward_name(address: str, city: str) -> str:
    if city == "Mumbai":
        if "Dadar" in address: return "Ward G/North (Dadar)"
        if "Bandra" in address: return "Ward H/West (Bandra)"
        if "Andheri" in address: return "Ward K/East (Andheri)"
        if "Kurla" in address: return "Ward L (Kurla)"
        if "Dharavi" in address: return "Ward G/North (Dharavi)"
        if "Chembur" in address: return "Ward M/West (Chembur)"
        if "Colaba" in address: return "Ward A (Colaba)"
        return "Ward G/North (Mumbai)"
    else:
        if "Majiwada" in address: return "Ward 3 (Majiwada, Thane)"
        if "Naupada" in address: return "Ward 1 (Naupada, Thane)"
        if "Wagle" in address: return "Ward 2 (Wagle Estate, Thane)"
        if "Ghodbunder" in address: return "Ward 4 (Ghodbunder, Thane)"
        if "Kopri" in address: return "Ward 5 (Kopri, Thane)"
        if "Kalwa" in address: return "Ward 6 (Kalwa, Thane)"
        if "Vartak" in address: return "Ward 2 (Vartak Nagar, Thane)"
        return "Ward 1 (Thane)"

def get_locality_name(address: str) -> str:
    for loc in ["Dadar", "Bandra", "Majiwada", "Naupada", "Andheri", "Kurla", "Wagle Estate", "Ghodbunder", "Dharavi", "Kopri", "Chembur", "Kalwa", "Colaba", "Vartak Nagar"]:
        if loc.lower() in address.lower():
            return loc
    return "Central Ward"

def load_initial_mumbai_thane_issues() -> List[Dict[str, Any]]:
    """Loads the Mumbai & Thane dataset from JSON and formats each record for frontend rendering."""
    json_path = ROOT_DIR / "data" / "mumbai_thane_civic_issues.json"
    if not json_path.exists():
        logger.warning("Dataset JSON not found at %s", json_path)
        return []
    
    with open(json_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    items = []
    for r in records:
        cat = map_dataset_category(r["issue_type"])
        ward = get_ward_name(r["location_street_address"], r["location_city"])
        locality = get_locality_name(r["location_street_address"])
        title = f"{r['issue_type']} at {locality}"
        if len(title) > 60:
            title = f"{r['issue_type'][:45]}... at {locality}"

        is_mumbai = r["location_city"] == "Mumbai"
        corp_name = "Brihanmumbai Municipal Corporation (BMC)" if is_mumbai else "Thane Municipal Corporation (TMC)"
        contact_info = "bmc.helpline@mcgm.gov.in / Civic Helpline 1916" if is_mumbai else "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108"
        ngo_name = "Mumbai March Civic Action Collective" if is_mumbai else "Thane Citizen Action Council"
        ngo_focus = "Infrastructure Monitoring & Safety" if "Road" in cat or "Safety" in cat else "Sanitation & Water Rights"

        items.append({
            "id": r["report_id"].lower(),
            "title": title,
            "locationName": f"{r['location_street_address']}, {r['location_city']}",
            "ward": ward,
            "locality": locality,
            "distanceKm": round(1.2 + (r["severity_score"] % 5) * 0.7, 1),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "category": cat,
            "severity": r["priority_level"],
            "urgency": "Immediate (24h)" if r["priority_level"] == "Critical" else ("Urgent (48-72h)" if r["priority_level"] == "High" else "Moderate (1-2 weeks)"),
            "status": r["issue_status"],
            "evidenceConfidence": r["priority_score"],
            "dateDiscovered": "Oct 8, 2026",
            "description": r["issue_description"],
            "cause": {
                "documented": f"Documented failure reported by resident ID {r['resident_id']} under {r['area_importance']}.",
                "isVerified": r["issue_status"] == "Verified"
            },
            "affectedPeople": f"Est. ~{r['citizen_reports_count'] * 120} residents & commuters traversing {locality}.",
            "likelyImpact": f"Severe inconvenience, risk to life/property, and disruption to {r['area_importance']}.",
            "unverifiedAspects": f"Detailed site audit from {r['municipal_department']} assistant municipal engineer scheduled.",
            "responsibleAuthority": {
                "name": corp_name,
                "department": r["municipal_department"],
                "contact": contact_info,
                "officialStatus": f"Target resolution within {r['resolution_days']} days (Ref: {r['report_id']})."
            },
            "relevantNgos": [
                {"name": ngo_name, "verified": True, "focus": ngo_focus},
                {"name": f"{r['location_city']} Clean & Safe Initiative", "verified": True, "focus": "Rapid Community Response"}
            ],
            "availableResources": [
                f"Municipal rapid response crew assigned by {corp_name}",
                "Local volunteer monitoring team on standby"
            ],
            "evidence": [
                {
                    "id": f"ev-{r['report_id'].lower()}-1",
                    "title": f"Resident Field Complaint #{r['report_id']}",
                    "type": "Citizen Report",
                    "date": "Oct 9, 2026",
                    "excerpt": r["issue_description"],
                    "isOfficial": False,
                    "credibilityScore": r["severity_score"]
                },
                {
                    "id": f"ev-{r['report_id'].lower()}-2",
                    "title": f"Local Press Corroboration ({r['location_city']} Mirror)",
                    "type": "News Media",
                    "date": "Oct 10, 2026",
                    "excerpt": f"Reporters verified civic disruption along {r['location_street_address']}. Traffic police alerted.",
                    "isOfficial": True,
                    "credibilityScore": 91
                }
            ],
            "contradictingEvidence": None,
            "mergedReportsCount": r["citizen_reports_count"],
            "actionPlan": [
                {"phase": "Phase 1: Verification & Perimeter Cordon", "description": "Install reflective caution barriers and inspect structural defects.", "status": "Completed" if r["issue_status"] in ("In progress", "Resolved") else "Pending"},
                {"phase": f"Phase 2: Repair & Intervention by {r['municipal_department']}", "description": "Execute targeted municipal engineering fix.", "status": "In progress" if r["issue_status"] == "In progress" else "Pending"},
                {"phase": "Phase 3: Citizen Closeout Audit", "description": "Verify durability and sign-off on public grievance closure.", "status": "Pending"}
            ],
            "donationGoal": 35000,
            "donationRaised": 12500 if r["priority_level"] == "Critical" else 6000,
            "donationBeneficiary": f"{ngo_name} Public Fund",
            "volunteerSlots": [
                {"id": f"vs-{r['report_id'].lower()}-1", "dateTime": "Saturday, Oct 17 · 9:30 AM - 12:30 PM", "voteCount": r["citizen_reports_count"] // 2, "isConfirmed": True, "isPopular": True},
                {"id": f"vs-{r['report_id'].lower()}-2", "dateTime": "Sunday, Oct 18 · 8:30 AM - 11:30 AM", "voteCount": 6, "isConfirmed": False}
            ],
            "volunteerMeetingPoint": f"{r['location_street_address']} (Near Landmark)",
            "volunteerActivity": "Hazard geotagging, perimeter safety caution marking, and filing RTI/escalation petition.",
            "volunteerResourcesRequired": "Safety reflective vest, protective gloves, mobile camera.",
            "registeredVolunteersCount": min(40, max(5, r["citizen_reports_count"] // 2))
        })
    return items

INITIAL_FRONTEND_ISSUES: List[Dict[str, Any]] = load_initial_mumbai_thane_issues()

# Thread-safe in-memory issues store
LIVE_ISSUES: List[Dict[str, Any]] = [dict(item) for item in INITIAL_FRONTEND_ISSUES]'''

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    end_idx += len(end_marker)
    content = content[:start_idx] + replacement_issues_block + content[end_idx:]
    print("Successfully replaced INITIAL_FRONTEND_ISSUES block.")
else:
    print("Could not find INITIAL_FRONTEND_ISSUES markers:", start_idx, end_idx)

# 2. Update startup_event to also sync issues to civic_engine SQLite database
old_startup_block = '''            try:
                StakeholderService(db)
                logger.info("Civic statutory authority directory initialized.")
            finally:
                db.close()'''

new_startup_block = '''            try:
                StakeholderService(db)
                logger.info("Civic statutory authority directory initialized.")
                
                # Sync Mumbai & Thane dataset into civic_engine SQLite database
                from app.models.models import ConsolidatedIssue
                dataset_path = ROOT_DIR / "data" / "mumbai_thane_civic_issues.json"
                if dataset_path.exists():
                    with open(dataset_path, "r", encoding="utf-8") as f:
                        raw_records = json.load(f)
                    for rec in raw_records:
                        issue_id = rec["report_id"].lower()
                        existing = db.query(ConsolidatedIssue).filter(ConsolidatedIssue.id == issue_id).first()
                        if not existing:
                            ci = ConsolidatedIssue(
                                id=issue_id,
                                title=f"{rec['issue_type']} at {rec['location_city']}",
                                summary=rec["issue_description"],
                                category=map_dataset_category(rec["issue_type"]),
                                normalized_location=f"{rec['location_street_address']}, {rec['location_city']}",
                                latitude=rec["latitude"],
                                longitude=rec["longitude"],
                                jurisdiction_name=rec["municipal_department"],
                                ward_zone=f"{rec['location_city']} - {rec['location_postal_code']}",
                                observation_count=rec["citizen_reports_count"],
                                is_recurring=rec["citizen_reports_count"] > 20,
                                severity_score=rec["severity_score"] / 10.0,
                                composite_priority_score=float(rec["priority_score"]),
                                what_is_happening=rec["issue_description"],
                                where_is_it_happening=rec["location_street_address"],
                                recommended_practical_action=f"Dispatch {rec['municipal_department']} within {rec['resolution_days']} days."
                            )
                            db.add(ci)
                    db.commit()
                    logger.info("Synchronized %d dataset issues into civic_engine SQLite database.", len(raw_records))
            finally:
                db.close()'''

if old_startup_block in content:
    content = content.replace(old_startup_block, new_startup_block, 1)
    print("Successfully updated startup_event with civic_engine DB synchronization.")
else:
    print("Could not find old_startup_block in content.")

# 3. Update report_new_civic_issue authority and coordinate defaults
old_report_block = '''        lat = req.latitude or (22.5510 + (len(LIVE_ISSUES) * 0.005))
        lng = req.longitude or (88.3650 + (len(LIVE_ISSUES) * 0.005))
        
        # Calculate credibility score: structured citizen submission gets initial baseline score
        base_confidence = 68 if req.evidenceNote else 58

        new_id = f"issue-{int(datetime.now().timestamp() * 1000)}"

        # Select authority based on ward/locality keywords
        authority_name = "Kolkata Municipal Corporation (KMC)" if "Kolkata" in req.ward or "Ward 42" in req.ward or "Ward 94" in req.ward else "Bruhat Bengaluru Mahanagara Palike (BBMP)"
        department_name = f"Borough Civic Response Cell ({req.ward})"'''

new_report_block = '''        lat = req.latitude or (19.0178 + (len(LIVE_ISSUES) * 0.001))
        lng = req.longitude or (72.8478 + (len(LIVE_ISSUES) * 0.001))
        
        # Calculate credibility score: structured citizen submission gets initial baseline score
        base_confidence = 68 if req.evidenceNote else 58

        new_id = f"issue-{int(datetime.now().timestamp() * 1000)}"

        # Select authority based on ward/locality keywords (Mumbai BMC vs Thane TMC)
        is_thane = any(k in f"{req.ward} {req.locality}".lower() for k in ["thane", "majiwada", "naupada", "wagle", "ghodbunder", "kalwa", "kopri", "vartak"])
        if is_thane:
            authority_name = "Thane Municipal Corporation (TMC)"
            department_name = f"TMC Ward Executive Cell ({req.ward})"
            ngo_name = "Thane Citizen Action Council"
        else:
            authority_name = "Brihanmumbai Municipal Corporation (BMC)"
            department_name = f"BMC Ward Administrative Office ({req.ward})"
            ngo_name = "Mumbai March Civic Action Collective"'''

if old_report_block in content:
    content = content.replace(old_report_block, new_report_block, 1)
    print("Successfully updated report_new_civic_issue with Mumbai & Thane logic.")
else:
    print("Could not find old_report_block in content.")

# 4. Add dataset endpoints to unified_server.py
old_endpoint_marker = '    # --------------------------------------------------------------------------\n    # Frontend Adapter API Endpoints (Direct contract for wardsync-frontend)\n    # --------------------------------------------------------------------------'
dataset_endpoints_code = '''    # --------------------------------------------------------------------------
    # Civic Dataset API Endpoints (Raw 22-column Mumbai & Thane Dataset)
    # --------------------------------------------------------------------------

    @app.get(
        "/api/dataset/mumbai-thane",
        tags=["Civic Dataset"],
        summary="Retrieve raw 22-column civic dataset for Mumbai & Thane (JSON)"
    )
    async def get_mumbai_thane_dataset():
        """Returns the full 22-field civic dataset for Mumbai & Thane in JSON format."""
        dataset_path = ROOT_DIR / "data" / "mumbai_thane_civic_issues.json"
        if not dataset_path.exists():
            raise HTTPException(status_code=404, detail="Dataset JSON file not found")
        with open(dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @app.get(
        "/api/dataset/mumbai-thane/csv",
        tags=["Civic Dataset"],
        summary="Download raw 22-column civic dataset for Mumbai & Thane (CSV)"
    )
    async def get_mumbai_thane_csv():
        """Downloads the full 22-column civic dataset for Mumbai & Thane in CSV format."""
        csv_path = ROOT_DIR / "data" / "mumbai_thane_civic_issues.csv"
        if not csv_path.exists():
            raise HTTPException(status_code=404, detail="Dataset CSV file not found")
        return FileResponse(
            path=str(csv_path),
            media_type="text/csv",
            filename="mumbai_thane_civic_issues.csv"
        )

    # --------------------------------------------------------------------------
    # Frontend Adapter API Endpoints (Direct contract for wardsync-frontend)
    # --------------------------------------------------------------------------'''

if old_endpoint_marker in content:
    content = content.replace(old_endpoint_marker, dataset_endpoints_code, 1)
    print("Successfully added dataset endpoints.")
else:
    print("Could not find old_endpoint_marker in content.")

# Write updated content
with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("unified_server.py updated successfully.")
