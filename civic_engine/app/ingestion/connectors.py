"""Source connectors for web pages, RSS feeds, uploaded files, and datasets."""

import abc
import datetime
import logging
from typing import List, Dict, Any, Optional
import feedparser
import httpx

from app.core.config import settings
from app.core.exceptions import IngestionError, UnsupportedFileTypeError
from app.core.security import calculate_content_hash
from app.ingestion.parsers import parse_pdf, parse_docx, parse_csv, parse_html_content, parse_plain_text

logger = logging.getLogger(__name__)


class NormalizedSourceData:
    """Standardized intermediate data structure produced by all connectors."""
    def __init__(
        self,
        source_type: str,
        original_title: str,
        extracted_text: str,
        original_url_or_ref: Optional[str] = None,
        publisher: Optional[str] = None,
        publication_date: Optional[datetime.datetime] = None,
        language: str = "en",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.source_type = source_type
        self.original_title = original_title
        self.extracted_text = extracted_text
        self.original_url_or_ref = original_url_or_ref
        self.publisher = publisher or "Unknown Publisher"
        self.publication_date = publication_date or datetime.datetime.utcnow()
        self.language = language
        self.metadata = metadata or {}
        self.content_hash = calculate_content_hash(extracted_text)


class BaseSourceConnector(abc.ABC):
    """Abstract base connector for acquiring and normalizing source data."""

    @abc.abstractmethod
    def ingest(self, *args, **kwargs) -> List[NormalizedSourceData]:
        pass


class DirectTextConnector(BaseSourceConnector):
    """Ingests raw text directly provided by user or API payload."""

    def ingest(self, title: str, text: str, publisher: str = "Direct Submission", metadata: Optional[Dict[str, Any]] = None) -> List[NormalizedSourceData]:
        if not text or not text.strip():
            raise IngestionError("Submitted text is empty.")
        return [
            NormalizedSourceData(
                source_type="user_text",
                original_title=title,
                extracted_text=text.strip(),
                original_url_or_ref="direct_submission",
                publisher=publisher,
                publication_date=datetime.datetime.utcnow(),
                metadata=metadata or {},
            )
        ]


class FileUploadConnector(BaseSourceConnector):
    """Parses uploaded file binary content (PDF, DOCX, CSV, TXT, MD)."""

    def ingest(self, filename: str, file_bytes: bytes, publisher: str = "Uploaded Document") -> List[NormalizedSourceData]:
        ext = "." + filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise UnsupportedFileTypeError(f"File extension '{ext}' is not supported. Allowed: {settings.ALLOWED_EXTENSIONS}")

        if ext == ".pdf":
            text = parse_pdf(file_bytes)
            source_type = "pdf"
        elif ext == ".docx":
            text = parse_docx(file_bytes)
            source_type = "docx"
        elif ext == ".csv":
            text = parse_csv(file_bytes)
            source_type = "csv"
        elif ext in [".txt", ".md", ".json", ".xml"]:
            text = parse_plain_text(file_bytes)
            source_type = ext.replace(".", "")
        else:
            raise UnsupportedFileTypeError(f"Unsupported file format: {ext}")

        return [
            NormalizedSourceData(
                source_type=source_type,
                original_title=filename,
                extracted_text=text,
                original_url_or_ref=f"upload://{filename}",
                publisher=publisher,
                metadata={"filename": filename, "file_size_bytes": len(file_bytes)},
            )
        ]


class WebPageConnector(BaseSourceConnector):
    """Fetches and parses public webpages with ethical headers and timeouts."""

    def ingest(self, url: str, publisher_override: Optional[str] = None) -> List[NormalizedSourceData]:
        headers = {
            "User-Agent": "CivicIssueDiscoveryBot/1.0 (+https://example.org/civic-bot; public interest civic monitoring)"
        }
        try:
            with httpx.Client(timeout=float(settings.REQUEST_TIMEOUT_SECONDS), follow_redirects=True, headers=headers) as client:
                resp = client.get(url)
                resp.raise_for_status()
                html_text = resp.text

            title, clean_text = parse_html_content(html_text)
            publisher = publisher_override or url.split("//")[-1].split("/")[0]

            return [
                NormalizedSourceData(
                    source_type="news_web",
                    original_title=title,
                    extracted_text=clean_text,
                    original_url_or_ref=url,
                    publisher=publisher,
                    metadata={"source_url": url, "http_status": 200},
                )
            ]
        except Exception as e:
            logger.error(f"Failed to fetch webpage at {url}: {e}")
            raise IngestionError(f"Failed to retrieve web source from {url}: {e}")


class RSSFeedConnector(BaseSourceConnector):
    """Fetches and normalizes RSS / Atom feeds."""

    def ingest(self, feed_url: str, max_entries: int = 15) -> List[NormalizedSourceData]:
        try:
            headers = {"User-Agent": "CivicIssueDiscoveryBot/1.0"}
            with httpx.Client(timeout=float(settings.REQUEST_TIMEOUT_SECONDS), headers=headers) as client:
                resp = client.get(feed_url)
                resp.raise_for_status()
                feed_content = resp.text

            feed = feedparser.parse(feed_content)
            feed_title = getattr(feed.feed, "title", "Civic RSS Feed")
            results = []

            for entry in feed.entries[:max_entries]:
                item_title = getattr(entry, "title", "Untitled Item")
                item_link = getattr(entry, "link", feed_url)
                item_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
                pub_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = datetime.datetime(*entry.published_parsed[:6])

                body_text = f"{item_title}\n\n{item_summary}"
                results.append(
                    NormalizedSourceData(
                        source_type="rss",
                        original_title=item_title,
                        extracted_text=body_text,
                        original_url_or_ref=item_link,
                        publisher=feed_title,
                        publication_date=pub_date,
                        metadata={"feed_url": feed_url, "guid": getattr(entry, "id", item_link)},
                    )
                )

            return results
        except Exception as e:
            logger.error(f"Failed to parse RSS feed from {feed_url}: {e}")
            raise IngestionError(f"Failed to ingest RSS feed: {e}")
