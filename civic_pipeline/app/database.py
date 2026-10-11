import math
import logging
from datetime import datetime, date, timezone
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4

from .config import get_settings

logger = logging.getLogger("civic_pipeline.database")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two float vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class InMemoryDatabaseRepository:
    """
    In-memory stateful repository simulating Supabase + pgvector.
    Used for local testing, CI, and zero-dependency standalone execution.
    """
    def __init__(self):
        self.sources: Dict[str, Dict[str, Any]] = {}
        self.issues: Dict[str, Dict[str, Any]] = {}
        self.ngos: Dict[str, Dict[str, Any]] = {}
        self.events: Dict[str, Dict[str, Any]] = {}
        self._seed_default_ngos()

    def _seed_default_ngos(self):
        """Seed default verified NGOs matching the migration script."""
        default_ngos = [
            {
                "id": "c1111111-1111-4111-8111-111111111111",
                "name": "CleanCity Green Action Foundation",
                "primary_causes": ["Sanitation", "Environment"],
                "operating_wards": ["Koramangala Ward 151", "Indiranagar Ward 82", "HSR Layout Ward 174"],
                "contact_email": "contact@cleancity.org",
                "is_verified": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "c2222222-2222-4222-8222-222222222222",
                "name": "SafeRoads & Rapid Drainage Collective",
                "primary_causes": ["Roads & Transit", "Waterlogging", "Public Safety"],
                "operating_wards": ["Koramangala Ward 151", "Whitefield Ward 84", "Bellandur Ward 150"],
                "contact_email": "actions@saferoads.org",
                "is_verified": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "c3333333-3333-4333-8333-333333333333",
                "name": "Bangalore Water Watch & Flood Response",
                "primary_causes": ["Waterlogging", "Environment", "Public Safety"],
                "operating_wards": ["HSR Layout Ward 174", "Bellandur Ward 150", "Marathahalli Ward 85"],
                "contact_email": "alert@waterwatch.ngo",
                "is_verified": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        for ngo in default_ngos:
            self.ngos[ngo["id"]] = ngo

    # --- Civic Sources ---
    def insert_source(self, data: Dict[str, Any]) -> Dict[str, Any]:
        item_id = str(data.get("id") or uuid4())
        record = {
            **data,
            "id": item_id,
            "created_at": data.get("created_at") or datetime.now(timezone.utc).isoformat(),
            "status": data.get("status", "raw")
        }
        self.sources[item_id] = record
        return record

    def update_source(self, source_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        sid = str(source_id)
        if sid in self.sources:
            self.sources[sid].update(updates)
            return self.sources[sid]
        return None

    def get_sources_by_issue(self, issue_id: str) -> List[Dict[str, Any]]:
        iid = str(issue_id)
        return [s for s in self.sources.values() if str(s.get("issue_id")) == iid]

    # --- Civic Issues ---
    def insert_issue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        issue_id = str(data.get("id") or uuid4())
        record = {
            **data,
            "id": issue_id,
            "created_at": data.get("created_at") or datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self.issues[issue_id] = record
        return record

    def update_issue(self, issue_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        iid = str(issue_id)
        if iid in self.issues:
            self.issues[iid].update(updates)
            self.issues[iid]["updated_at"] = datetime.now(timezone.utc).isoformat()
            return self.issues[iid]
        return None

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        return self.issues.get(str(issue_id))

    def search_similar_issues(
        self,
        query_embedding: List[float],
        similarity_threshold: float = 0.82,
        match_count: int = 5,
        filter_ward: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Simulate pgvector cosine distance match_similar_civic_issues stored function."""
        results = []
        for issue in self.issues.values():
            embedding = issue.get("embedding")
            if not embedding:
                continue
            if filter_ward and issue.get("ward") != filter_ward:
                continue
            
            sim = cosine_similarity(query_embedding, embedding)
            if sim >= similarity_threshold:
                result_item = dict(issue)
                result_item["similarity"] = round(sim, 4)
                results.append(result_item)

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:match_count]

    # --- NGOs ---
    def get_ngo(self, ngo_id: str) -> Optional[Dict[str, Any]]:
        return self.ngos.get(str(ngo_id))

    def list_ngos(self) -> List[Dict[str, Any]]:
        return list(self.ngos.values())

    def find_matching_ngos(self, ward: str, category: str) -> List[Dict[str, Any]]:
        matches = []
        for ngo in self.ngos.values():
            if not ngo.get("is_verified", True):
                continue
            wards = ngo.get("operating_wards", [])
            causes = ngo.get("primary_causes", [])
            if ward in wards and category in causes:
                matches.append(ngo)
        return matches

    # --- NGO Volunteer Events ---
    def insert_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        event_id = str(data.get("id") or uuid4())
        record = {
            **data,
            "id": event_id,
            "registered_volunteers": data.get("registered_volunteers", 0),
            "status": data.get("status", "draft"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self.events[event_id] = record
        return record

    def update_event(self, event_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        eid = str(event_id)
        if eid in self.events:
            self.events[eid].update(updates)
            self.events[eid]["updated_at"] = datetime.now(timezone.utc).isoformat()
            return self.events[eid]
        return None

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        return self.events.get(str(event_id))

    def get_events_by_issue(self, issue_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        iid = str(issue_id)
        results = [e for e in self.events.values() if str(e.get("issue_id")) == iid]
        if status:
            results = [e for e in results if e.get("status") == status]
        return results

    def get_events_by_ngo(self, ngo_id: str) -> List[Dict[str, Any]]:
        nid = str(ngo_id)
        return [e for e in self.events.values() if str(e.get("ngo_id")) == nid]

    def get_all_active_map_clusters(self) -> List[Dict[str, Any]]:
        """Return verified issues that have published/active volunteer events."""
        results = []
        for issue in self.issues.values():
            iid = str(issue["id"])
            active_events = [
                e for e in self.events.values() 
                if str(e.get("issue_id")) == iid and e.get("status") in ("published", "completed")
            ]
            if active_events or issue.get("status") == "event_active":
                enriched_events = []
                for ev in active_events:
                    ngo = self.ngos.get(str(ev["ngo_id"]), {})
                    enriched_events.append({
                        "event_id": ev["id"],
                        "ngo_id": ev["ngo_id"],
                        "ngo_name": ngo.get("name", "Local Civic Action NGO"),
                        "event_title": ev["event_title"],
                        "event_date": ev["event_date"],
                        "meeting_point": ev["meeting_point"],
                        "target_volunteers": ev["target_volunteers"],
                        "registered_volunteers": ev.get("registered_volunteers", 0),
                        "required_gear": ev.get("required_gear", []),
                        "tasks_breakdown": ev.get("tasks_breakdown", []),
                        "safety_guidelines": ev.get("safety_guidelines", []),
                        "status": ev["status"]
                    })
                item = dict(issue)
                item["active_events"] = enriched_events
                results.append(item)
        return results


class SupabaseDatabaseRepository:
    """
    Production repository communicating with Supabase PostgreSQL + pgvector.
    Uses supabase-py client and RPC stored functions.
    """
    def __init__(self, supabase_url: str, supabase_key: str):
        from supabase import create_client, Client
        self.client: Client = create_client(supabase_url, supabase_key)
        logger.info("Initialized Supabase live connection to %s", supabase_url)

    def insert_source(self, data: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.table("civic_sources").insert(data).execute()
        return resp.data[0] if resp.data else data

    def update_source(self, source_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        resp = self.client.table("civic_sources").update(updates).eq("id", str(source_id)).execute()
        return resp.data[0] if resp.data else None

    def get_sources_by_issue(self, issue_id: str) -> List[Dict[str, Any]]:
        resp = self.client.table("civic_sources").select("*").eq("issue_id", str(issue_id)).execute()
        return resp.data or []

    def insert_issue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.table("civic_issues").insert(data).execute()
        return resp.data[0] if resp.data else data

    def update_issue(self, issue_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        resp = self.client.table("civic_issues").update(updates).eq("id", str(issue_id)).execute()
        return resp.data[0] if resp.data else None

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        resp = self.client.table("civic_issues").select("*").eq("id", str(issue_id)).execute()
        return resp.data[0] if resp.data else None

    def search_similar_issues(
        self,
        query_embedding: List[float],
        similarity_threshold: float = 0.82,
        match_count: int = 5,
        filter_ward: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        params = {
            "query_embedding": query_embedding,
            "similarity_threshold": similarity_threshold,
            "match_count": match_count,
            "filter_ward": filter_ward
        }
        resp = self.client.rpc("match_similar_civic_issues", params).execute()
        return resp.data or []

    def get_ngo(self, ngo_id: str) -> Optional[Dict[str, Any]]:
        resp = self.client.table("ngos").select("*").eq("id", str(ngo_id)).execute()
        return resp.data[0] if resp.data else None

    def list_ngos(self) -> List[Dict[str, Any]]:
        resp = self.client.table("ngos").select("*").execute()
        return resp.data or []

    def find_matching_ngos(self, ward: str, category: str) -> List[Dict[str, Any]]:
        # Query verified NGOs where operating_wards contains ward and primary_causes contains category
        resp = self.client.table("ngos")\
            .select("*")\
            .eq("is_verified", True)\
            .contains("operating_wards", [ward])\
            .contains("primary_causes", [category])\
            .execute()
        return resp.data or []

    def insert_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.table("ngo_volunteer_events").insert(data).execute()
        return resp.data[0] if resp.data else data

    def update_event(self, event_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        resp = self.client.table("ngo_volunteer_events").update(updates).eq("id", str(event_id)).execute()
        return resp.data[0] if resp.data else None

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        resp = self.client.table("ngo_volunteer_events").select("*").eq("id", str(event_id)).execute()
        return resp.data[0] if resp.data else None

    def get_events_by_issue(self, issue_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.client.table("ngo_volunteer_events").select("*").eq("issue_id", str(issue_id))
        if status:
            query = query.eq("status", status)
        resp = query.execute()
        return resp.data or []

    def get_events_by_ngo(self, ngo_id: str) -> List[Dict[str, Any]]:
        resp = self.client.table("ngo_volunteer_events").select("*").eq("ngo_id", str(ngo_id)).execute()
        return resp.data or []

    def get_all_active_map_clusters(self) -> List[Dict[str, Any]]:
        # Fetch issues with status event_active or join published events
        issues_resp = self.client.table("civic_issues").select("*").in_("status", ["verified_pending_ngo", "event_active"]).execute()
        issues = issues_resp.data or []
        results = []
        for issue in issues:
            events_resp = self.client.table("ngo_volunteer_events")\
                .select("*, ngos(name)")\
                .eq("issue_id", issue["id"])\
                .in_("status", ["published", "completed"])\
                .execute()
            events = events_resp.data or []
            if events or issue.get("status") == "event_active":
                enriched_events = []
                for ev in events:
                    ngo_data = ev.get("ngos") or {}
                    enriched_events.append({
                        "event_id": ev["id"],
                        "ngo_id": ev["ngo_id"],
                        "ngo_name": ngo_data.get("name", "Local Civic Action NGO"),
                        "event_title": ev["event_title"],
                        "event_date": ev["event_date"],
                        "meeting_point": ev["meeting_point"],
                        "target_volunteers": ev["target_volunteers"],
                        "registered_volunteers": ev.get("registered_volunteers", 0),
                        "required_gear": ev.get("required_gear", []),
                        "tasks_breakdown": ev.get("tasks_breakdown", []),
                        "safety_guidelines": ev.get("safety_guidelines", []),
                        "status": ev["status"]
                    })
                item = dict(issue)
                item["active_events"] = enriched_events
                results.append(item)
        return results


# Global repository instance
_repo_instance = None


def get_repository():
    """Retrieve configured database repository singleton."""
    global _repo_instance
    if _repo_instance is None:
        settings = get_settings()
        if settings.is_supabase_configured:
            try:
                _repo_instance = SupabaseDatabaseRepository(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("Using live Supabase repository.")
            except Exception as e:
                logger.warning("Failed to initialize live Supabase repository: %s. Falling back to in-memory store.", e)
                _repo_instance = InMemoryDatabaseRepository()
        else:
            logger.info("Supabase not configured or placeholder detected. Operating in high-fidelity in-memory mode.")
            _repo_instance = InMemoryDatabaseRepository()
    return _repo_instance


def reset_repository_for_testing():
    """Utility for unit tests to reset repository state."""
    global _repo_instance
    _repo_instance = InMemoryDatabaseRepository()
    return _repo_instance
