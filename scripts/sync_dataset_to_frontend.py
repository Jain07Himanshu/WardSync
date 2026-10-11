"""Converts the Mumbai & Thane dataset into sampleIssues.ts for the frontend."""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT_DIR / "data" / "mumbai_thane_civic_issues.json"
TARGET_TS = ROOT_DIR / "wardsync-frontend" / "src" / "data" / "sampleIssues.ts"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    records = json.load(f)

# Helper category mapper
def map_category(issue_type):
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

# Helper ward identifier
def get_ward(address, city):
    if city == "Mumbai":
        if "Dadar" in address: return "Ward G/North (Dadar)"
        if "Bandra" in address: return "Ward H/West (Bandra)"
        if "Andheri" in address: return "Ward K/East (Andheri)"
        if "Kurla" in address: return "Ward L (Kurla)"
        if "Dharavi" in address: return "Ward G/North (Dharavi)"
        if "Chembur" in address: return "Ward M/West (Chembur)"
        if "Colaba" in address: return "Ward A (Colaba)"
        return "Ward G/North (Mumbai)"
    else: # Thane
        if "Majiwada" in address: return "Ward 3 (Majiwada, Thane)"
        if "Naupada" in address: return "Ward 1 (Naupada, Thane)"
        if "Wagle" in address: return "Ward 2 (Wagle Estate, Thane)"
        if "Ghodbunder" in address: return "Ward 4 (Ghodbunder, Thane)"
        if "Kopri" in address: return "Ward 5 (Kopri, Thane)"
        if "Kalwa" in address: return "Ward 6 (Kalwa, Thane)"
        if "Vartak" in address: return "Ward 2 (Vartak Nagar, Thane)"
        return "Ward 1 (Thane)"

# Helper locality identifier
def get_locality(address):
    for loc in ["Dadar", "Bandra", "Majiwada", "Naupada", "Andheri", "Kurla", "Wagle Estate", "Ghodbunder", "Dharavi", "Kopri", "Chembur", "Kalwa", "Colaba", "Vartak Nagar"]:
        if loc.lower() in address.lower():
            return loc
    return "Central Ward"

frontend_issues = []

for r in records:
    cat = map_category(r["issue_type"])
    ward = get_ward(r["location_street_address"], r["location_city"])
    locality = get_locality(r["location_street_address"])
    
    # Title formatting
    title = f"{r['issue_type']} at {locality}"
    if len(title) > 60:
        title = f"{r['issue_type'][:45]}... at {locality}"

    is_mumbai = r["location_city"] == "Mumbai"
    corp_name = "Brihanmumbai Municipal Corporation (BMC)" if is_mumbai else "Thane Municipal Corporation (TMC)"
    contact_info = "bmc.helpline@mcgm.gov.in / Civic Helpline 1916" if is_mumbai else "tmc.callcenter@thanecity.gov.in / Helpline 1800-222-108"

    ngo_name = "Mumbai March Civic Action Collective" if is_mumbai else "Thane Citizen Action Council"
    ngo_focus = "Infrastructure Monitoring & Safety" if "Road" in cat or "Safety" in cat else "Sanitation & Water Rights"

    issue_obj = {
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
    }
    frontend_issues.append(issue_obj)

# Output TypeScript file
ts_content = f"""import {{ Issue }} from '../types';

export const SAMPLE_ISSUES: Issue[] = {json.dumps(frontend_issues, indent=2)};
"""

with open(TARGET_TS, "w", encoding="utf-8") as f:
    f.write(ts_content)

print(f"Successfully synced {len(frontend_issues)} Mumbai/Thane issues to {TARGET_TS}")
