# Frontend Integration Guide

The Civic Issue Discovery & Action Engine is completely decoupled from any frontend. It exposes versioned REST endpoints ready for consumption by web dashboards, citizen mobile applications, or municipal workflow portals.

---

## 1. Quick Integration Steps

1. **Verify Backend Status**:
   `GET http://localhost:8000/api/v1/health`
2. **CORS Configuration**:
   CORS is pre-enabled for all origins (`*`) by default in `app/main.py`. For production, configure explicit allowed origins in `app/core/config.py`.
3. **Interactive Documentation**:
   Point your developers or OpenAPI code generator to `http://localhost:8000/openapi.json` to generate client SDKs automatically.

---

## 2. TypeScript Types Matching Backend Schemas

Save these TypeScript definitions into `types/civic.ts` in your frontend project:

```typescript
export interface ConsolidatedIssue {
  id: string;
  title: string;
  summary: string;
  category: string;
  subcategory?: string | null;
  normalized_location?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  jurisdiction_name?: string | null;
  ward_zone?: string | null;
  observation_count: number;
  distinct_publishers_count: number;
  first_seen_date?: string | null;
  last_seen_date?: string | null;
  is_recurring: boolean;
  recurrence_pattern: 'SINGLE_INCIDENT' | 'RECURRING_CHRONIC' | 'SEASONAL_MONSOON' | 'EXPANDING_CORRIDOR';
  trend_direction: 'NEW' | 'STABLE' | 'ESCALATING' | 'DECREASING' | 'RESOLVED';
  verification_level: 'SINGLE_UNVERIFIED' | 'CROSS_SOURCE_CORROBORATED' | 'OFFICIALLY_NOTIFIED';
  composite_priority_score: number;
  severity_score: number;
  urgency_score: number;
  recurrence_score: number;
  evidence_strength_score: number;
  community_impact_score: number;
  actionability_score: number;
  created_at: string;
}

export interface CivicOpportunity {
  id: string;
  issue_id: string;
  issue_title?: string | null;
  title: string;
  problem_summary: string;
  why_needed: string;
  activity_type: 'EVIDENCE_COLLECTION' | 'COMMUNITY_SURVEY' | 'OFFICIAL_GRIEVANCE_FILING' | 'AWARENESS_CAMPAIGN' | 'AUTHORIZED_CLEANUP' | 'ACCESSIBILITY_AUDIT' | 'PROGRESS_MONITORING';
  step_by_step_plan: string[];
  intended_beneficiaries?: string | null;
  suggested_roles: string[];
  required_materials: string[];
  estimated_effort_hours: number;
  suggested_participant_count: number;
  potential_collaborators: string[];
  escalation_channel?: string | null;
  expected_outcomes?: string | null;
  success_metrics?: string | null;
  safety_considerations: string[];
  prerequisites_and_permissions: string[];
  is_official_authorization_required: boolean;
  safety_risk_level: 'LOW' | 'MODERATE' | 'HIGH_REQUIRES_AUTHORITY';
  ai_confidence: number;
  review_status: 'PENDING_REVIEW' | 'APPROVED' | 'REJECTED' | 'MODIFIED';
  priority_score: number;
  priority_breakdown: Record<string, any>;
}

export interface Stakeholder {
  id: string;
  issue_id: string;
  candidate_name: string;
  department?: string | null;
  relevance_reason: string;
  jurisdiction_coverage?: string | null;
  official_website?: string | null;
  public_portal_url?: string | null;
  public_helpline?: string | null;
  public_email?: string | null;
  grievance_redressal_mechanism?: string | null;
  verification_status: 'VERIFIED_REGISTRY' | 'CANDIDATE_UNVERIFIED';
  confidence_level: number;
}
```

---

## 3. Example React / Next.js Data Fetching Hook

```typescript
// hooks/useCivicIssues.ts
import { useState, useEffect } from 'react';
import { ConsolidatedIssue } from '../types/civic';

export function useCivicIssues(category?: string, minPriority: number = 0) {
  const [issues, setIssues] = useState<ConsolidatedIssue[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchIssues() {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (minPriority > 0) params.append('min_priority', minPriority.toString());

        const res = await fetch(`http://localhost:8000/api/v1/issues?${params.toString()}`);
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        const data = await res.json();
        setIssues(data.items);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchIssues();
  }, [category, minPriority]);

  return { issues, loading, error };
}
```

---

## 4. Polling Asynchronous Jobs in Frontend

When uploading documents or triggering discovery, the engine returns a `job_id`:

```typescript
async function pollJobStatus(jobId: string, onComplete: (summary: any) => void) {
  const interval = setInterval(async () => {
    const res = await fetch(`http://localhost:8000/api/v1/jobs/${jobId}`);
    const job = await res.json();
    if (job.status === 'COMPLETED') {
      clearInterval(interval);
      onComplete(job.result_summary);
    } else if (job.status === 'FAILED') {
      clearInterval(interval);
      console.error('Job failed:', job.error_details);
    }
  }, 1500);
}
```
