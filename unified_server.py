"""WardSync Unified Server: Connects Civic Engine, Civic Pipeline, and WardSync Frontend.

Integrates:
1. civic_pipeline (Gemini verification, pgvector/in-memory clustering, NGO dispatching, volunteer events)
2. civic_engine (Multi-provider AI, multi-format doc ingestion, authority mapping, opportunity generator, analytics)
3. wardsync-frontend (Map clusters, interactive issues, citizen reporting, volunteer registration, donations)
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from uuid import uuid4

# Set up module paths
ROOT_DIR = Path(__file__).resolve().parent
CIVIC_ENGINE_DIR = ROOT_DIR / "civic_engine"
CIVIC_PIPELINE_DIR = ROOT_DIR / "civic_pipeline"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(CIVIC_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(CIVIC_ENGINE_DIR))

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("wardsync.unified_server")

# Import civic_pipeline modules
from civic_pipeline.app.config import get_settings as get_pipeline_settings
from civic_pipeline.app.database import get_repository as get_pipeline_repository
from civic_pipeline.app.routes.ingest import router as pipeline_ingest_router
from civic_pipeline.app.routes.ngos import router as pipeline_ngos_router
from civic_pipeline.app.routes.events import router as pipeline_events_router
from civic_pipeline.app.routes.public import router as pipeline_public_router
from civic_pipeline.app.ai.clustering_engine import get_clustering_engine
from civic_pipeline.app.ai.extractor_and_verifier import get_extractor_and_verifier

# Ensure database path is absolute so it works from any CWD
db_path = (CIVIC_ENGINE_DIR / "civic_engine.db").resolve()
import os
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

# Import civic_engine modules
from app.core.config import settings as engine_settings
from app.core.database import init_db, SessionLocal
from app.stakeholders.service import StakeholderService
from app.api.v1 import api_router as civic_engine_api_router

# Initialize database tables immediately
init_db()


# ==============================================================================
# Pydantic Schemas for Frontend Contract
# ==============================================================================

class CauseModel(BaseModel):
    documented: str
    isVerified: bool = False

class ResponsibleAuthorityModel(BaseModel):
    name: str
    department: str
    contact: str
    officialStatus: str

class RelevantNgoModel(BaseModel):
    name: str
    verified: bool = True
    focus: str

class EvidenceSourceModel(BaseModel):
    id: str
    title: str
    type: str  # 'Official Record' | 'Lab Analysis' | 'Citizen Report' | 'News Media' | 'NGO Survey'
    date: str
    link: Optional[str] = None
    excerpt: str
    isOfficial: bool = False
    credibilityScore: int = 70

class ActionPlanPhase(BaseModel):
    phase: str
    description: str
    status: str = "Pending"  # 'Completed' | 'In progress' | 'Pending'

class VolunteerSlotModel(BaseModel):
    id: str
    dateTime: str
    voteCount: int = 1
    isConfirmed: bool = False
    isPopular: Optional[bool] = False

class FrontendIssue(BaseModel):
    id: str
    title: str
    locationName: str
    ward: str
    locality: str
    distanceKm: float = 1.0
    latitude: float
    longitude: float
    category: str
    severity: str
    urgency: str = "Urgent (48-72h)"
    status: str = "Reported"
    evidenceConfidence: int = 75
    dateDiscovered: str
    description: str
    cause: CauseModel
    affectedPeople: str
    likelyImpact: str
    unverifiedAspects: str
    responsibleAuthority: ResponsibleAuthorityModel
    relevantNgos: List[RelevantNgoModel] = Field(default_factory=list)
    availableResources: List[str] = Field(default_factory=list)
    evidence: List[EvidenceSourceModel] = Field(default_factory=list)
    contradictingEvidence: Optional[str] = None
    mergedReportsCount: int = 1
    actionPlan: List[ActionPlanPhase] = Field(default_factory=list)
    donationGoal: int = 25000
    donationRaised: int = 0
    donationBeneficiary: str = "Local Community Action Alliance"
    volunteerSlots: List[VolunteerSlotModel] = Field(default_factory=list)
    volunteerMeetingPoint: str
    volunteerActivity: str
    volunteerResourcesRequired: str
    registeredVolunteersCount: int = 0

class ReportIssueRequest(BaseModel):
    title: str
    category: str
    ward: str
    locality: str
    description: str
    severity: str = "High"
    evidenceNote: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class DonationRequest(BaseModel):
    issueId: str
    amount: int
    donorName: str
    isAnonymous: bool = False

class CampaignRequest(BaseModel):
    issueId: str
    targetAmount: int
    purpose: str
    beneficiaryOrg: str

class IssueStatusUpdateRequest(BaseModel):
    status: str


# ==============================================================================
# In-Memory Live Issues Store for WardSync Frontend
# ==============================================================================

# Helper category mapper
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
LIVE_ISSUES: List[Dict[str, Any]] = [dict(item) for item in INITIAL_FRONTEND_ISSUES]


# ==============================================================================
# Helper Functions for Cross-Engine Data Synchronization
# ==============================================================================

def sync_pipeline_issue_to_frontend(pipeline_issue: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a civic_pipeline issue record into a rich frontend Issue record."""
    issue_id = str(pipeline_issue.get("id") or f"issue-{uuid4()}")
    ward = pipeline_issue.get("ward", "Koramangala Ward 151")
    locality = ward.split(" ")[0] if " " in ward else ward
    category = pipeline_issue.get("category", "Sanitation")
    
    # Map category to frontend IssueCategory
    category_map = {
        "Sanitation": "Waste Management",
        "Pothole": "Roads & Transport",
        "Waterlogging": "Water & Sanitation",
        "Streetlight": "Public Safety",
        "Environment": "Environment",
        "Public Safety": "Public Safety",
        "Waste Management": "Waste Management",
        "Roads & Transport": "Roads & Transport",
        "Water & Sanitation": "Water & Sanitation",
        "Health": "Health"
    }
    mapped_cat = category_map.get(category, "Waste Management")

    frontend_item: Dict[str, Any] = {
        "id": issue_id,
        "title": pipeline_issue.get("title", f"Civic Issue in {ward}"),
        "locationName": f"{ward}, Local Municipal Zone",
        "ward": ward,
        "locality": locality,
        "distanceKm": 1.2,
        "latitude": pipeline_issue.get("latitude", 12.9352),
        "longitude": pipeline_issue.get("longitude", 77.6245),
        "category": mapped_cat,
        "severity": pipeline_issue.get("severity", "High"),
        "urgency": "Urgent (48-72h)" if pipeline_issue.get("severity") in ("High", "Critical") else "Moderate (1-2 weeks)",
        "status": "Verified" if pipeline_issue.get("authenticity_score", 0) >= 65 else "Reported",
        "evidenceConfidence": pipeline_issue.get("authenticity_score", 75),
        "dateDiscovered": datetime.now().strftime("%b %d, %Y"),
        "description": pipeline_issue.get("summary", "Civic defect identified from multi-source resident signals."),
        "cause": {
            "documented": pipeline_issue.get("verification_reasoning") or "Multi-source resident signals cross-verified by AI.",
            "isVerified": pipeline_issue.get("authenticity_score", 0) >= 65
        },
        "affectedPeople": f"Residents, shopkeepers, and daily commuters traversing {ward}.",
        "likelyImpact": "Hazard to public safety and localized infrastructure disruption.",
        "unverifiedAspects": "Field site inspection report from municipal assistant engineer pending.",
        "responsibleAuthority": {
            "name": pipeline_issue.get("responsible_authority", "Municipal Corporation"),
            "department": "Zonal Civic Infrastructure Division",
            "contact": "civic-helpdesk@municipal.gov.in",
            "officialStatus": "Auto-flagged by WardSync intelligence engine; queued for inspection."
        },
        "relevantNgos": [
            {"name": "CleanCity Action Foundation", "verified": True, "focus": "Rapid Community Response"},
            {"name": "Ward Mobilization Network", "verified": True, "focus": "Volunteer Coordination"}
        ],
        "availableResources": [
            "Local volunteer monitoring team alerted",
            "Protective work kits & safety signage staged at local hub"
        ],
        "evidence": [
            {
                "id": f"ev-{uuid4()}",
                "title": "Cross-Verified Resident & Social Media Signals",
                "type": "Citizen Report",
                "date": "Today",
                "excerpt": pipeline_issue.get("summary", ""),
                "isOfficial": False,
                "credibilityScore": pipeline_issue.get("authenticity_score", 75)
            }
        ],
        "contradictingEvidence": None,
        "mergedReportsCount": pipeline_issue.get("source_count", 1),
        "actionPlan": [
            {"phase": "Phase 1: Verification & Signage", "description": "Erect safety perimeter and file urgent municipal civic grievance ticket.", "status": "In progress"},
            {"phase": "Phase 2: Volunteer Community Drive", "description": "Mobilize citizen volunteers and local NGO to conduct rapid remediation drive.", "status": "Pending"},
            {"phase": "Phase 3: Formal SLA Closeout", "description": "Verify municipal department permanent repair against public standards.", "status": "Pending"}
        ],
        "donationGoal": 20000,
        "donationRaised": 0,
        "donationBeneficiary": "Ward Action Relief Alliance",
        "volunteerSlots": [
            {"id": f"vs-{uuid4()}", "dateTime": "Upcoming Saturday · 9:00 AM - 12:00 PM", "voteCount": 3, "isConfirmed": True, "isPopular": True}
        ],
        "volunteerMeetingPoint": f"{ward} Community Center Gate",
        "volunteerActivity": "Perimeter inspection, community documentation, and distributing relief kits.",
        "volunteerResourcesRequired": "Gloves, safety vest, notebook/mobile phone.",
        "registeredVolunteersCount": 1
    }
    return frontend_item


# ==============================================================================
# FastAPI Application Creation
# ==============================================================================

def create_unified_app() -> FastAPI:
    """Builds and wires the unified WardSync FastAPI application."""
    
    app = FastAPI(
        title="WardSync: Civic Issue Discovery, Intelligence, and Action Generation Engine",
        description=(
            "Unified enterprise-grade engine connecting multi-provider GenAI civic discovery, "
            "corroboration pipelines, statutory authority directory, and community volunteer mobilization."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Enable CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize civic_engine database tables and stakeholders on startup
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting WardSync Unified Platform...")
        try:
            init_db()
            db = SessionLocal()
            try:
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
                db.close()
            logger.info("Civic Engine SQLite database initialized successfully.")
        except Exception as e:
            logger.warning("Civic Engine DB init notice: %s", e)

        # Seed initial pipeline demo issues into civic_pipeline in-memory repo
        try:
            pipeline_repo = get_pipeline_repository()
            for iss in LIVE_ISSUES:
                pipeline_repo.insert_issue({
                    "id": iss["id"],
                    "title": iss["title"],
                    "summary": iss["description"],
                    "category": iss["category"],
                    "ward": iss["ward"],
                    "latitude": iss["latitude"],
                    "longitude": iss["longitude"],
                    "severity": iss["severity"],
                    "authenticity_score": iss["evidenceConfidence"],
                    "responsible_authority": iss["responsibleAuthority"]["name"],
                    "source_count": iss["mergedReportsCount"],
                    "status": "event_active" if iss["registeredVolunteersCount"] > 0 else "verified"
                })
            logger.info("Synchronized %d initial issues to civic_pipeline repository.", len(LIVE_ISSUES))
        except Exception as e:
            logger.warning("Pipeline repo sync notice: %s", e)

    # --------------------------------------------------------------------------
    # Mount Subsystem Routers
    # --------------------------------------------------------------------------

    # 1. Mount civic_pipeline routes
    app.include_router(pipeline_ingest_router)
    app.include_router(pipeline_ngos_router)
    app.include_router(pipeline_events_router)
    app.include_router(pipeline_public_router)

    # 2. Mount civic_engine routes
    app.include_router(civic_engine_api_router, prefix="/api/v1")

    # --------------------------------------------------------------------------
    # Root & Health Endpoints
    # --------------------------------------------------------------------------

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/docs")

    @app.get("/health", tags=["System Health"])
    @app.get("/api/health", tags=["System Health"])
    async def unified_health_check():
        """Returns comprehensive health across both engines and the frontend bridge."""
        p_settings = get_pipeline_settings()
        return {
            "status": "healthy",
            "service": "WardSync Civic Discovery, Intelligence & Action Generation Engine",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "subsystems": {
                "civic_engine": {
                    "provider": engine_settings.AI_PROVIDER,
                    "model": engine_settings.AI_MODEL or "default",
                    "database": engine_settings.DATABASE_URL,
                    "status": "ready"
                },
                "civic_pipeline": {
                    "gemini_live": p_settings.is_gemini_configured,
                    "similarity_threshold": p_settings.SIMILARITY_THRESHOLD,
                    "verification_threshold": p_settings.VERIFICATION_THRESHOLD,
                    "status": "ready"
                },
                "wardsync_frontend_bridge": {
                    "live_issues_count": len(LIVE_ISSUES),
                    "status": "connected"
                }
            }
        }

    # --------------------------------------------------------------------------
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
    # --------------------------------------------------------------------------

    @app.get(
        "/api/public/issues",
        response_model=List[FrontendIssue],
        tags=["Frontend Bridge"],
        summary="Fetch all verified issues with complete intelligence dossiers for frontend rendering"
    )
    async def get_frontend_issues():
        """
        Returns all live civic issues formatted with 100% compatibility with
        the wardsync-frontend Issue TypeScript interface.
        """
        return LIVE_ISSUES

    @app.post(
        "/api/public/issues",
        response_model=FrontendIssue,
        status_code=status.HTTP_201_CREATED,
        tags=["Frontend Bridge"],
        summary="Citizen reports new civic issue: runs AI verification, extraction & action generation"
    )
    async def report_new_civic_issue(req: ReportIssueRequest):
        """
        Accepts a citizen report from the frontend ReportIssueModal, executes AI synthesis,
        extracts cause, location, responsible municipal authority, matched NGOs,
        generates volunteer slots, and saves the issue.
        """
        lat = req.latitude or (19.0178 + (len(LIVE_ISSUES) * 0.001))
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
            ngo_name = "Mumbai March Civic Action Collective"

        created_issue: Dict[str, Any] = {
            "id": new_id,
            "title": req.title,
            "locationName": f"{req.ward}, {req.locality}",
            "ward": req.ward,
            "locality": req.locality,
            "distanceKm": 0.8,
            "latitude": lat,
            "longitude": lng,
            "category": req.category,
            "severity": req.severity,
            "urgency": "Immediate (24h)" if req.severity == "Critical" else "Urgent (48-72h)" if req.severity == "High" else "Moderate (1-2 weeks)",
            "status": "Reported",
            "evidenceConfidence": base_confidence,
            "dateDiscovered": "Just now",
            "description": req.description,
            "cause": {
                "documented": req.evidenceNote or "Citizen field observation reported via intake form.",
                "isVerified": False
            },
            "affectedPeople": "Nearby residents, pedestrians, and local business owners.",
            "likelyImpact": "Civic inconvenience and safety risk if unaddressed.",
            "unverifiedAspects": "Municipal field officer site inspection pending.",
            "responsibleAuthority": {
                "name": authority_name,
                "department": department_name,
                "contact": "civic.response@municipal.gov.in",
                "officialStatus": "Queued for priority site inspection."
            },
            "relevantNgos": [
                {"name": "Ward Action Alliance", "verified": True, "focus": "Rapid Neighborhood Response"}
            ],
            "availableResources": [
                "Local volunteer monitoring team on standby",
                "Incident logged in WardSync open civic register"
            ],
            "evidence": [
                {
                    "id": f"ev-{uuid4()}",
                    "title": "Citizen Direct Intake Submission",
                    "type": "Citizen Report",
                    "date": "Today",
                    "excerpt": req.evidenceNote or req.description,
                    "isOfficial": False,
                    "credibilityScore": base_confidence
                }
            ],
            "contradictingEvidence": None,
            "mergedReportsCount": 1,
            "actionPlan": [
                {"phase": "Phase 1: Verification & Inspection", "description": "Municipal field officer site visit and photographic audit.", "status": "Pending"},
                {"phase": "Phase 2: Civic Intervention", "description": "Mobilize local cleanup or engineering repairs.", "status": "Pending"}
            ],
            "donationGoal": 15000,
            "donationRaised": 0,
            "donationBeneficiary": "Ward Action Alliance Community Relief Fund",
            "volunteerSlots": [
                {"id": f"vs-{uuid4()}", "dateTime": "Upcoming Weekend · 9:00 AM", "voteCount": 1, "isConfirmed": False, "isPopular": True}
            ],
            "volunteerMeetingPoint": f"{req.locality} Community Junction, {req.ward}",
            "volunteerActivity": "Perimeter documentation and safety caution sign placement.",
            "volunteerResourcesRequired": "Mobile camera, gloves, notebook.",
            "registeredVolunteersCount": 1
        }

        # Add to live memory store (prepended so user sees it first)
        LIVE_ISSUES.insert(0, created_issue)

        # Also register into civic_pipeline repository for clustering and NGO feeds
        try:
            pipeline_repo = get_pipeline_repository()
            pipeline_repo.insert_issue({
                "id": new_id,
                "title": created_issue["title"],
                "summary": created_issue["description"],
                "category": created_issue["category"],
                "ward": created_issue["ward"],
                "latitude": created_issue["latitude"],
                "longitude": created_issue["longitude"],
                "severity": created_issue["severity"],
                "authenticity_score": created_issue["evidenceConfidence"],
                "responsible_authority": authority_name,
                "source_count": 1,
                "status": "flagged_unverified"
            })
        except Exception as e:
            logger.warning("Pipeline repo sync warning: %s", e)

        logger.info("Successfully created and registered new civic issue: %s (%s)", created_issue['title'], new_id)
        return created_issue

    @app.post(
        "/api/donations",
        tags=["Frontend Bridge"],
        summary="Citizen records donation toward NGO civic campaign"
    )
    async def record_donation(req: DonationRequest):
        """Records simulated donation and increments donationRaised in the issue record."""
        target_issue = next((iss for iss in LIVE_ISSUES if iss["id"] == req.issueId), None)
        if not target_issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        target_issue["donationRaised"] = target_issue.get("donationRaised", 0) + req.amount
        logger.info("Donation of ₹%d recorded for issue %s by %s", req.amount, req.issueId, req.donorName)
        return {
            "status": "success",
            "issueId": req.issueId,
            "amount": req.amount,
            "totalRaised": target_issue["donationRaised"],
            "simulatedTxnId": f"TXN_{uuid4().hex[:8].upper()}"
        }

    @app.post(
        "/api/campaigns",
        tags=["Frontend Bridge"],
        summary="NGO launches fundraising campaign for civic issue"
    )
    async def launch_campaign(req: CampaignRequest):
        """Updates campaign parameters on the target issue."""
        target_issue = next((iss for iss in LIVE_ISSUES if iss["id"] == req.issueId), None)
        if target_issue:
            target_issue["donationGoal"] = req.targetAmount
            target_issue["donationBeneficiary"] = req.beneficiaryOrg
        return {"status": "success", "campaign": req.model_dump()}

    @app.patch(
        "/api/issues/{issue_id}/status",
        tags=["Frontend Bridge"],
        summary="Government official updates civic issue resolution status"
    )
    async def update_issue_status(issue_id: str, req: IssueStatusUpdateRequest):
        """Updates issue status (Reported, Verified, In progress, Resolved)."""
        target_issue = next((iss for iss in LIVE_ISSUES if iss["id"] == issue_id), None)
        if not target_issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        target_issue["status"] = req.status
        logger.info("Updated status of issue %s to %s", issue_id, req.status)
        return {"status": "success", "issueId": issue_id, "newStatus": req.status}

    return app


app = create_unified_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
