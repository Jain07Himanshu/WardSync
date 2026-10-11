"""Ingestion Service for normalizing and persisting incoming source records."""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.models import Source, AuditEvent
from app.ingestion.connectors import (
    NormalizedSourceData,
    DirectTextConnector,
    FileUploadConnector,
    WebPageConnector,
    RSSFeedConnector,
)

logger = logging.getLogger(__name__)


class IngestionService:
    """Orchestrates document parsing, hashing, deduplication, and database persistence."""

    def __init__(self, db: Session):
        self.db = db
        self.text_connector = DirectTextConnector()
        self.file_connector = FileUploadConnector()
        self.web_connector = WebPageConnector()
        self.rss_connector = RSSFeedConnector()

    def persist_normalized_sources(self, items: List[NormalizedSourceData]) -> List[Source]:
        """Save normalized sources to database, skipping identical content hashes idempotently."""
        saved_sources = []
        for item in items:
            # Check for existing content hash
            existing = self.db.query(Source).filter(Source.content_hash == item.content_hash).first()
            if existing:
                logger.info(f"Duplicate content detected for hash {item.content_hash} (existing source id: {existing.id})")
                saved_sources.append(existing)
                continue

            # Create new source
            source = Source(
                source_type=item.source_type,
                original_title=item.original_title,
                original_url_or_ref=item.original_url_or_ref,
                publisher=item.publisher,
                publication_date=item.publication_date,
                extracted_text=item.extracted_text,
                language=item.language,
                content_hash=item.content_hash,
                processing_status="PENDING",
                metadata_payload=item.metadata,
            )
            self.db.add(source)
            self.db.flush()

            # Record audit event
            audit = AuditEvent(
                event_type="SOURCE_INGESTED",
                entity_type="Source",
                entity_id=source.id,
                details={
                    "source_type": source.source_type,
                    "title": source.original_title,
                    "publisher": source.publisher,
                    "content_length": len(source.extracted_text),
                }
            )
            self.db.add(audit)
            saved_sources.append(source)

        self.db.commit()
        return saved_sources

    def ingest_text(self, title: str, text: str, publisher: str = "Direct Submission", metadata: Optional[Dict[str, Any]] = None) -> Source:
        items = self.text_connector.ingest(title=title, text=text, publisher=publisher, metadata=metadata)
        return self.persist_normalized_sources(items)[0]

    def ingest_file(self, filename: str, file_bytes: bytes, publisher: str = "Uploaded Document") -> Source:
        items = self.file_connector.ingest(filename=filename, file_bytes=file_bytes, publisher=publisher)
        return self.persist_normalized_sources(items)[0]

    def ingest_url(self, url: str, publisher: Optional[str] = None) -> Source:
        items = self.web_connector.ingest(url=url, publisher_override=publisher)
        return self.persist_normalized_sources(items)[0]

    def ingest_rss(self, feed_url: str, max_entries: int = 15) -> List[Source]:
        items = self.rss_connector.ingest(feed_url=feed_url, max_entries=max_entries)
        return self.persist_normalized_sources(items)
