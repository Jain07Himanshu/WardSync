"""Deterministic Mock AI Provider for testing and offline development."""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.providers.base import BaseAIProvider
from app.schemas.common import CivicCategory, ActivityType, IssueRelationshipType
from app.schemas.issue import ExtractedIssueSchema
from app.schemas.stakeholder import StakeholderRecommendationSchema
from app.schemas.opportunity import CivicActionPlanSchema


class MockAIProvider(BaseAIProvider):
    """
    Deterministic AI Provider returning validated, realistic mock civic intelligence.
    Enables full end-to-end testing and offline evaluation without API key costs.
    """

    @property
    def provider_name(self) -> str:
        return "mock"

    def analyze_source(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        has_hindi = bool(re.search(r"[\u0900-\u097F]", source_text))
        lang = "mr" if ("आहे" in source_text or "पाणी" in source_text or "रस्ता" in source_text) else ("hi" if has_hindi else "en")

        return {
            "summary": "Mock civic intelligence overview of source document.",
            "detected_language": lang,
            "relevance_score": 0.88,
            "contains_civic_complaint": True,
            "potential_locations": ["Andheri West", "Link Road", "S.V. Road", "Bandra East"],
            "ai_provider": "mock",
            "mock_mode": True,
        }

    def extract_civic_issues(self, source_text: str, metadata: Optional[Dict[str, Any]] = None) -> List[ExtractedIssueSchema]:
        text_lower = source_text.lower()
        extracted: List[ExtractedIssueSchema] = []

        # 1. Potholes / Roads
        if any(w in text_lower for w in ["pothole", "crater", "road repair", "asphalt", "गड्डा", "खड्डे", "रस्ता"]):
            extracted.append(
                ExtractedIssueSchema(
                    issue_title="Severe Potholes and Road Surface Disrepair",
                    problem_description="Deep potholes and asphalt disintegration observed along the roadway, slowing vehicular traffic and endangering two-wheelers.",
                    category=CivicCategory.ROADS_AND_POTHOLES.value,
                    subcategory="Potholes and bitumen erosion",
                    location_mentioned="S.V. Road near Andheri West railway station junction",
                    normalized_location="S.V. Road, Andheri West, Mumbai",
                    latitude=19.1197,
                    longitude=72.8468,
                    affected_population="Daily vehicular commuters, bus passengers, and local shopkeepers",
                    first_reported_date="2026-09-15",
                    most_recent_observation_date="2026-10-05",
                    possible_causes=["Heavy monsoon precipitation", "Sub-standard resurfacing bitumen mixture", "Heavy axle vehicle transit"],
                    reported_consequences=["Severe traffic snarls during peak hours", "Two-wheeler skidding risk", "Vehicle suspension damage"],
                    evidence_excerpts=["Multiple large craters extending up to 6 inches deep have appeared on the arterial corridor.", "Commuters complain of spine-jarring journeys."],
                    source_references=[metadata.get("title", "Civic Source Report") if metadata else "Local Citizen Dispatch"],
                    confidence_score=0.92,
                    missing_information=["Specific municipal contractor warranty details", "Exact municipal maintenance contract number"],
                    verification_status="COMMUNITY_REPORTED",
                    suggested_next_steps=["Conduct photographic measurement audit", "Lodge formal complaint on BMC 24x7 grievance portal"],
                )
            )

        # 2. Waterlogging / Drainage
        if any(w in text_lower for w in ["waterlog", "drainage", "storm water", "flooding", "nallah", "नाला", "पाणी साचले"]):
            extracted.append(
                ExtractedIssueSchema(
                    issue_title="Monsoon Waterlogging and Storm Drain Choking",
                    problem_description="Storm water drains clogged with uncollected debris causing persistent water accumulation up to knee-level after rainfall.",
                    category=CivicCategory.DRAINAGE_AND_WATERLOGGING.value,
                    subcategory="Stormwater drain blockage and siltation",
                    location_mentioned="Hindmata Junction and Milan Subway, Mumbai",
                    normalized_location="Milan Subway, Santacruz West, Mumbai",
                    latitude=19.0833,
                    longitude=72.8367,
                    affected_population="Low-lying residential colonies and subway vehicular traffic",
                    first_reported_date="2026-08-20",
                    most_recent_observation_date="2026-10-02",
                    possible_causes=["Incomplete desilting of major storm drains", "Plastic packaging waste clogging intake grates"],
                    reported_consequences=["Complete vehicular closure of subway during heavy downpours", "Backflow into ground-floor residences"],
                    evidence_excerpts=["Water levels rose to 2 feet within thirty minutes of downpour due to choked drainage grates."],
                    source_references=[metadata.get("title", "Civic Source Report") if metadata else "Monsoon Preparedness Dispatch"],
                    confidence_score=0.90,
                    missing_information=["Status of high-capacity dewatering pumps installed at subway entrance"],
                    verification_status="CORROBORATED",
                    suggested_next_steps=["Verify operational readiness of suction pumps", "Inspect drain catch-pits along approach ramp"],
                )
            )

        # 3. Waste Management / Garbage
        if any(w in text_lower for w in ["garbage", "trash", "waste", "dumping", "litter", "कचरा", "डंपिंग"]):
            extracted.append(
                ExtractedIssueSchema(
                    issue_title="Uncontrolled Open Solid Waste Dumping and Irregular Clearance",
                    problem_description="Accumulation of unsegregated municipal solid waste in vacant roadside plots, producing foul odor and attracting stray animals.",
                    category=CivicCategory.WASTE_MANAGEMENT.value,
                    subcategory="Illegal roadside dumping and irregular collection",
                    location_mentioned="Near Link Road intersection, Malad West",
                    normalized_location="Link Road, Malad West, Mumbai",
                    latitude=19.1865,
                    longitude=72.8375,
                    affected_population="Nearby residential housing societies and pedestrians",
                    first_reported_date="2026-09-01",
                    most_recent_observation_date="2026-10-08",
                    possible_causes=["Lack of designated community waste collection bins", "Failure of contractor compactors to adhere to daily morning schedule"],
                    reported_consequences=["Severe foul odor spreading to residential balconies", "Health hazard from disease vectors like flies and mosquitoes"],
                    evidence_excerpts=["Garbage has remained uncollected for over four consecutive days, spilling onto the active carriageway."],
                    source_references=[metadata.get("title", "Civic Source Report") if metadata else "Solid Waste Monitoring Report"],
                    confidence_score=0.88,
                    missing_information=["Ward Solid Waste Management (SWM) supervisor contact roster"],
                    verification_status="COMMUNITY_REPORTED",
                    suggested_next_steps=["Lodge photo-tagged complaint on civic Swachhata app", "Engage local RWA for segregated collection"],
                )
            )

        # 4. Water Supply
        if any(w in text_lower for w in ["water supply", "contamination", "pipeline leak", "drinking water", "पाणी पुरवठा", "जल प्रदूषण"]):
            extracted.append(
                ExtractedIssueSchema(
                    issue_title="Low Water Pressure and Intermittent Pipeline Contamination",
                    problem_description="Residents report muddy, foul-smelling tap water with inadequate supply pressure lasting only 30 minutes daily.",
                    category=CivicCategory.WATER_SUPPLY_AND_QUALITY.value,
                    subcategory="Drinking water contamination and pressure loss",
                    location_mentioned="Sector 4, Ghodbunder Road, Thane",
                    normalized_location="Ghodbunder Road, Thane West",
                    latitude=19.2616,
                    longitude=72.9667,
                    affected_population="Over 2,500 apartment units and local commercial clinics",
                    first_reported_date="2026-09-28",
                    most_recent_observation_date="2026-10-09",
                    possible_causes=["Cross-contamination with sewage line due to corroded underground pipeline joint"],
                    reported_consequences=["Cases of water-borne gastroenteritis reported in local clinics", "High dependency on expensive private water tankers"],
                    evidence_excerpts=["Turbid yellowish water flowed from kitchen taps, leading residents to boil all drinking water."],
                    source_references=[metadata.get("title", "Civic Source Report") if metadata else "Public Health & Water Watch"],
                    confidence_score=0.91,
                    missing_information=["Bacteriological water testing lab report from municipal lab"],
                    verification_status="COMMUNITY_REPORTED",
                    suggested_next_steps=["Collect tap water sample for certified lab testing", "Escalate to Municipal Hydraulic Engineer"],
                )
            )

        # Fallback if no specific trigger matched
        if not extracted:
            extracted.append(
                ExtractedIssueSchema(
                    issue_title="Reported Civic Infrastructure Deficiency",
                    problem_description=f"Identified civic disrepair in source dispatch: {source_text[:200]}...",
                    category=CivicCategory.OTHER_EMERGING_CONCERNS.value,
                    subcategory="General municipal amenity deficiency",
                    location_mentioned="Reported Urban Ward Corridor",
                    normalized_location="Mumbai Metropolitan Region",
                    latitude=19.0760,
                    longitude=72.8777,
                    affected_population="Local residents and general public",
                    first_reported_date=datetime.utcnow().strftime("%Y-%m-%d"),
                    most_recent_observation_date=datetime.utcnow().strftime("%Y-%m-%d"),
                    possible_causes=["Delayed periodic municipal maintenance"],
                    reported_consequences=["Inconvenience to pedestrians and residents"],
                    evidence_excerpts=[source_text[:150]],
                    source_references=["Analyzed Source Dispatch"],
                    confidence_score=0.75,
                    missing_information=["Specific ward boundary and department jurisdiction"],
                    verification_status="UNVERIFIED",
                    suggested_next_steps=["Conduct ground verification of reported deficiency"],
                )
            )

        return extracted

    def classify_issue(self, issue_description: str) -> Dict[str, Any]:
        text_lower = issue_description.lower()
        if "pothole" in text_lower or "road" in text_lower:
            return {"category": CivicCategory.ROADS_AND_POTHOLES.value, "subcategory": "Potholes and road surface", "confidence": 0.95}
        elif "water" in text_lower and ("supply" in text_lower or "pipe" in text_lower):
            return {"category": CivicCategory.WATER_SUPPLY_AND_QUALITY.value, "subcategory": "Potable water supply", "confidence": 0.92}
        elif "flood" in text_lower or "drain" in text_lower:
            return {"category": CivicCategory.DRAINAGE_AND_WATERLOGGING.value, "subcategory": "Drainage systems", "confidence": 0.93}
        elif "garbage" in text_lower or "waste" in text_lower:
            return {"category": CivicCategory.WASTE_MANAGEMENT.value, "subcategory": "Solid waste disposal", "confidence": 0.94}
        return {"category": CivicCategory.OTHER_EMERGING_CONCERNS.value, "subcategory": "General public amenity", "confidence": 0.70}

    def find_related_issues(self, target_issue: Dict[str, Any], candidate_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        target_loc = (target_issue.get("normalized_location") or "").lower()
        target_cat = (target_issue.get("category") or "").lower()

        for cand in candidate_issues:
            cand_id = cand.get("id", "")
            cand_loc = (cand.get("normalized_location") or "").lower()
            cand_cat = (cand.get("category") or "").lower()

            same_cat = (target_cat == cand_cat)
            same_loc = bool(target_loc and cand_loc and (target_loc in cand_loc or cand_loc in target_loc))

            if same_cat and same_loc:
                results.append({
                    "target_issue_id": cand_id,
                    "target_title": cand.get("title", ""),
                    "relationship_type": IssueRelationshipType.RECURRING_INCIDENT.value,
                    "similarity_score": 0.88,
                    "match_reasons": ["Matching civic category", "Same geographic location / corridor", "Consistent recurring complaint"],
                })
            elif same_cat:
                results.append({
                    "target_issue_id": cand_id,
                    "target_title": cand.get("title", ""),
                    "relationship_type": IssueRelationshipType.CROSS_AREA_SIMILAR.value,
                    "similarity_score": 0.65,
                    "match_reasons": ["Identical civic category across different wards", "Common municipal governance failure pattern"],
                })
            else:
                results.append({
                    "target_issue_id": cand_id,
                    "target_title": cand.get("title", ""),
                    "relationship_type": IssueRelationshipType.UNRELATED_KEYWORD_MATCH.value,
                    "similarity_score": 0.20,
                    "match_reasons": ["Different civic categories and distinct locations"],
                })

        return results

    def identify_stakeholders(self, issue_data: Dict[str, Any], jurisdiction_info: Optional[Dict[str, Any]] = None) -> List[StakeholderRecommendationSchema]:
        category = issue_data.get("category", "")
        recommendations = []

        if category == CivicCategory.ROADS_AND_POTHOLES.value:
            recommendations.append(
                StakeholderRecommendationSchema(
                    organization_name="Brihanmumbai Municipal Corporation (BMC / MCGM)",
                    department="Roads and Traffic Department",
                    relevance_reason="Primary statutory authority responsible for maintenance, asphalt resurfacing, and pothole rectification on city arterial roads.",
                    jurisdiction_area="Mumbai Municipal Corporation Area",
                    verification_status="VERIFIED_REGISTRY",
                    confidence_level=0.95,
                    source_reference="MCGM Citizen Charter & Roads Manual",
                    public_portal_or_contact_hint="MCGM 24x7 Citizen Portal & BMC Pothole Tracking App (helpline 1916)",
                )
            )
            recommendations.append(
                StakeholderRecommendationSchema(
                    organization_name="Mumbai Traffic Police (Traffic Control Branch)",
                    department="Traffic Enforcement & Congestion Control",
                    relevance_reason="Jurisdictional police unit responsible for managing traffic diversions around damaged road sections to prevent bottlenecks.",
                    jurisdiction_area="Mumbai Traffic Police Commissionerate",
                    verification_status="VERIFIED_REGISTRY",
                    confidence_level=0.88,
                    source_reference="Maharashtra Police Regulations",
                    public_portal_or_contact_hint="Mumbai Traffic Police Helpline: 8454999999",
                )
            )
        elif category == CivicCategory.WASTE_MANAGEMENT.value:
            recommendations.append(
                StakeholderRecommendationSchema(
                    organization_name="Brihanmumbai Municipal Corporation (BMC)",
                    department="Solid Waste Management (SWM) Department",
                    relevance_reason="Statutory department in charge of primary collection, transportation, and clearing of municipal solid waste.",
                    jurisdiction_area="BMC Ward Office (Ward K-West / P-North)",
                    verification_status="VERIFIED_REGISTRY",
                    confidence_level=0.96,
                    source_reference="Solid Waste Management Rules 2016",
                    public_portal_or_contact_hint="Swachhata Citizen App & Ward SWM Control Room",
                )
            )
        else:
            recommendations.append(
                StakeholderRecommendationSchema(
                    organization_name="Local Ward Municipal Office",
                    department="Assistant Municipal Commissioner / Ward Officer",
                    relevance_reason="Zonal executive administrative officer responsible for civic grievance redressal and departmental coordination.",
                    jurisdiction_area=issue_data.get("normalized_location", "Local Civic Ward"),
                    verification_status="CANDIDATE_UNVERIFIED",
                    confidence_level=0.75,
                    source_reference="Municipal Ward Administration Directory",
                    public_portal_or_contact_hint="Official Ward Citizen Center Helpdesk",
                )
            )

        return recommendations

    def generate_civic_action(self, issue_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[CivicActionPlanSchema]:
        category = issue_data.get("category", "")
        plans = []

        if category == CivicCategory.ROADS_AND_POTHOLES.value:
            plans.append(
                CivicActionPlanSchema(
                    title="Community Pothole Documentation and Geo-Tagged Grievance Audit",
                    problem_summary="Substantial potholes along the road corridor create hazard for two-wheelers and pedestrians.",
                    why_needed="Official civic contractors frequently overlook smaller road defects until systematic photographic evidence is registered on official portals.",
                    activity_type=ActivityType.EVIDENCE_COLLECTION,
                    step_by_step_plan=[
                        "1. Assemble a volunteer audit team of 3-4 neighborhood residents during daylight non-peak hours.",
                        "2. Using mobile smartphones, take clear, geotagged photographs of road defects showing landmarks for precise location.",
                        "3. Use a standard ruler or measuring tape safely from the sidewalk to record estimated crater width and depth.",
                        "4. Log each defect on the official BMC Pothole Tracking App / 1916 helpline portal with exact GPS coordinates.",
                        "5. Collate all municipal complaint ticket tracking numbers into a shared neighborhood spreadsheet for weekly follow-up.",
                    ],
                    intended_beneficiaries="Two-wheeler riders, pedestrians, senior citizens, and ambulance drivers",
                    suggested_roles=["Lead Auditor", "Photo & GPS Logger", "Sidewalk Safety Lookout"],
                    required_materials=["Smartphones with GPS camera enabled", "High-visibility reflective safety vests", "Measuring tape", "Notepad/Clipboard"],
                    estimated_effort_hours=2.5,
                    suggested_participant_count=4,
                    potential_collaborators=["Local Residents Welfare Association (RWA)", "Active Commuters Group"],
                    escalation_channel="BMC Citizen Portal (1916) and Ward Assistant Commissioner Office",
                    expected_outcomes="Complete photographic dossier with official municipal complaint ticket numbers assigned to all defects.",
                    success_metrics="100% of identified potholes logged with verified ticket numbers within 24 hours.",
                    safety_considerations=[
                        "CRITICAL: Never step into active vehicular traffic or high-speed vehicle lanes.",
                        "Always conduct audits during clear daylight hours wearing bright reflective vests.",
                        "Keep at least one designated safety lookout monitoring incoming traffic.",
                        "Do not attempt any unauthorized road resurfacing or hazardous construction work.",
                    ],
                    prerequisites_and_permissions=["No municipal permit required for photography conducted safely from public sidewalks."],
                    is_official_authorization_required=False,
                    safety_risk_level="LOW",
                    ai_confidence=0.92,
                )
            )
        else:
            plans.append(
                CivicActionPlanSchema(
                    title="Neighborhood Civic Survey & Official Grievance Escalation",
                    problem_summary=f"Community concern regarding {issue_data.get('title', 'civic issue')}.",
                    why_needed="Consolidated citizen complaints backed by data have a 3x higher resolution rate with municipal bodies.",
                    activity_type=ActivityType.COMMUNITY_SURVEY,
                    step_by_step_plan=[
                        "1. Draft a concise 3-question survey documenting frequency and health/safety impact of the civic issue.",
                        "2. Collect survey inputs from at least 25 affected households or shop owners in the immediate vicinity.",
                        "3. Draft a formal memorandum with survey findings addressed to the Ward Officer.",
                        "4. Submit the memorandum via the official online grievance portal and obtain an acknowledgment receipt.",
                        "5. Schedule a 14-day progress review to verify whether municipal action has commenced.",
                    ],
                    intended_beneficiaries="Surrounding residents, children, and pedestrians",
                    suggested_roles=["Survey Lead", "Resident Liaison", "Grievance Coordinator"],
                    required_materials=["Digital survey form or paper clipboards", "Official grievance letter template"],
                    estimated_effort_hours=3.0,
                    suggested_participant_count=5,
                    potential_collaborators=["Local Apartment Association", "Civic Youth Club"],
                    escalation_channel="Municipal Ward Office Grievance Cell",
                    expected_outcomes="Verified citizen survey dataset submitted to ward authorities with registered tracking ID.",
                    success_metrics="At least 25 resident responses collected and official complaint reference generated.",
                    safety_considerations=[
                        "Respect resident privacy; do not publish personal phone numbers or names without consent.",
                        "Do not engage in confrontations with alleged violators or municipal field workers.",
                    ],
                    prerequisites_and_permissions=["Permission from building societies when surveying inside private residential complexes."],
                    is_official_authorization_required=False,
                    safety_risk_level="LOW",
                    ai_confidence=0.88,
                )
            )

        return plans

    def evaluate_evidence(self, issue_data: Dict[str, Any], evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        count = len(evidence_items)
        strength = min(10.0, 4.0 + (count * 2.0))
        corroboration = "Multi-source corroborated evidence" if count > 1 else "Single-source preliminary report"

        return {
            "evidence_count": count,
            "evidence_strength_score": strength,
            "corroboration_level": corroboration,
            "has_firsthand_quotes": True,
            "has_specific_dates": True,
            "missing_key_factors": ["Engineering inspection report", "Contractor accountability history"],
            "verification_recommendation": "Field verification recommended before major public campaign.",
            "ai_provider": "mock",
        }
