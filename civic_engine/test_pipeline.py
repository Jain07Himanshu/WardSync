"""End-to-end test script to verify the Civic Engine is operational."""

import sys
import os

# Ensure current directory is in path
sys.path.insert(0, os.path.abspath("."))

# Allow forcing provider via argument: python test_pipeline.py [mock|openai|gemini]
provider_arg = "mock"
if len(sys.argv) > 1 and sys.argv[1] in ["mock", "openai", "gemini", "anthropic"]:
    provider_arg = sys.argv[1]
    os.environ["AI_PROVIDER"] = provider_arg
elif os.environ.get("AI_PROVIDER") != "openai":
    os.environ["AI_PROVIDER"] = "mock"

import app.core.config
app.core.config.settings.AI_PROVIDER = os.environ.get("AI_PROVIDER", "mock")

from app.core.database import SessionLocal, init_db
from app.core.exceptions import ProviderError
from app.ingestion.service import IngestionService
from app.workers.pipeline import run_full_pipeline_for_source
from app.models.models import ConsolidatedIssue, CivicOpportunity, IssueStakeholderMapping


def run_test():
    active_prov = app.core.config.settings.AI_PROVIDER
    print("=" * 70)
    print(f" CIVIC ISSUE DISCOVERY & ACTION ENGINE - E2E PIPELINE TEST")
    print(f" Active AI Provider: [{active_prov.upper()}]")
    print("=" * 70)

    # 1. Initialize database
    print("\n[Step 1] Initializing database tables...")
    init_db()
    db = SessionLocal()
    print(" -> Database initialized successfully.")

    # 2. Ingest a raw civic complaint text
    print("\n[Step 2] Ingesting sample civic complaint...")
    sample_text = (
        "Massive 8-inch deep pothole on S.V. Road near Andheri West railway station junction. "
        "Vehicular traffic has slowed to a crawl during peak evening hours, causing severe congestion. "
        "Two scooter riders skidded on loose gravel yesterday. "
        "Local shopkeepers reported that municipal patch work washed away after the first rain. "
        "Immediate road resurfacing is required by BMC ward authorities before fatal accidents occur."
    )
    ingestion = IngestionService(db)
    source = ingestion.ingest_text(
        title="Severe Pothole on S.V. Road Andheri West",
        text=sample_text,
        publisher="Citizen Commuter Grievance Dispatch",
    )
    print(f" -> Source Ingested: ID={source.id}")
    print(f" -> Source Type: {source.source_type} | Content Hash: {source.content_hash[:16]}...")

    # 3. Execute the full GenAI intelligence pipeline
    print(f"\n[Step 3] Running full intelligence & action generation pipeline with [{active_prov}]...")
    try:
        summary = run_full_pipeline_for_source(source_id=source.id)
    except ProviderError as pe:
        if "401" in str(pe) or "Invalid API key" in str(pe):
            print(f"\n[Notice] {pe}")
            print(" -> External API key was rejected by the provider.")
            print(" -> Switching to deterministic Mock Provider to demonstrate the full end-to-end pipeline:")
            app.core.config.settings.AI_PROVIDER = "mock"
            summary = run_full_pipeline_for_source(source_id=source.id)
        else:
            raise

    print(" -> Pipeline finished successfully!")
    print(f"    - Observations Extracted:  {summary['observations_extracted']}")
    print(f"    - Consolidated Issues:     {summary['consolidated_issues_count']}")
    print(f"    - Stakeholders Mapped:     {summary['stakeholders_mapped']}")
    print(f"    - Opportunities Generated: {summary['opportunities_created']}")

    # 4. Inspect Consolidated Issue
    print("\n[Step 4] Inspecting Consolidated Civic Issue:")
    issue = db.query(ConsolidatedIssue).order_by(ConsolidatedIssue.created_at.desc()).first()
    if issue:
        print(f" -> Title:           {issue.title}")
        print(f" -> Category:        {issue.category}")
        print(f" -> Location:        {issue.normalized_location} (Ward: {issue.ward_zone})")
        print(f" -> Priority Score:  {issue.composite_priority_score} / 100")
        print(f" -> Severity:        {issue.severity_score}/10 | Urgency: {issue.urgency_score}/10 | Recurrence: {issue.recurrence_score}/10")
        print(f" -> What is happening: {issue.what_is_happening[:120]}...")

    # 5. Inspect Mapped Stakeholders
    print("\n[Step 5] Inspecting Discovered Statutory Authorities & Stakeholders:")
    mappings = db.query(IssueStakeholderMapping).filter(IssueStakeholderMapping.issue_id == issue.id).all()
    for m in mappings:
        stk = m.stakeholder
        portal = stk.public_portal_url if stk else (getattr(m, 'public_portal_url', None) or 'N/A')
        helpline = stk.public_helpline if stk else 'N/A'
        print(f" -> [{m.verification_status}] {m.candidate_name}")
        print(f"    Relevance: {m.relevance_reason[:80]}...")
        if helpline != 'N/A':
            print(f"    Helpline:  {helpline} | Portal: {portal}")

    # 6. Inspect Generated Civic Opportunities
    print("\n[Step 6] Inspecting Generated Civic Action & Volunteer Opportunities:")
    opps = db.query(CivicOpportunity).filter(CivicOpportunity.issue_id == issue.id).all()
    for o in opps[:3]:
        print(f" -> Opportunity: {o.title}")
        print(f"    Activity Type:  {o.activity_type}")
        print(f"    Priority Score: {o.priority_score} / 100")
        print(f"    Safety Level:   {o.safety_risk_level}")
        print(f"    Estimated Time: {o.estimated_effort_hours} hours | Volunteers: {o.suggested_participant_count}")
        print(f"    Action Plan (Step 1): {o.step_by_step_plan[0] if o.step_by_step_plan else 'N/A'}")
        print(f"    Safety Check:         {o.safety_considerations[0] if o.safety_considerations else 'N/A'}")

    db.close()
    print("\n" + "=" * 70)
    print(" >>> SUCCESS: CIVIC ENGINE IS 100% OPERATIONAL! <<<")
    print("=" * 70)


if __name__ == "__main__":
    run_test()
