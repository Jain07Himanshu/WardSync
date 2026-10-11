"""Document parsers for PDF, DOCX, CSV, TXT, and HTML content."""

import csv
import io
import logging
from typing import Tuple
from bs4 import BeautifulSoup

from app.core.exceptions import IngestionError

logger = logging.getLogger(__name__)


def parse_pdf(file_bytes: bytes) -> str:
    """Extract readable text from PDF bytes using pypdf."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages_text.append(text)
        extracted = "\n\n".join(pages_text).strip()
        if not extracted:
            return "[PDF contains no extractable text layer or is scanned image only]"
        return extracted
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise IngestionError(f"Failed to parse PDF document: {e}")


def parse_docx(file_bytes: bytes) -> str:
    """Extract text from Microsoft Word DOCX bytes using python-docx."""
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
        return "\n\n".join(paragraphs).strip()
    except Exception as e:
        logger.error(f"Error parsing DOCX: {e}")
        raise IngestionError(f"Failed to parse DOCX document: {e}")


def parse_csv(file_bytes: bytes, max_rows: int = 100) -> str:
    """Extract structured complaint records from CSV data."""
    try:
        content = file_bytes.decode("utf-8", errors="replace")
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        if not rows:
            return ""

        headers = rows[0]
        records = []
        for i, row in enumerate(rows[1:max_rows + 1]):
            row_dict = dict(zip(headers, row))
            summary_parts = [f"{k}: {v}" for k, v in row_dict.items() if v]
            records.append(f"Row {i+1}: " + ", ".join(summary_parts))

        res = f"CSV Headers: {', '.join(headers)}\n\n" + "\n".join(records)
        if len(rows) > max_rows:
            res += f"\n\n[Note: Truncated {len(rows) - max_rows} additional rows for initial extraction]"
        return res
    except Exception as e:
        logger.error(f"Error parsing CSV: {e}")
        raise IngestionError(f"Failed to parse CSV dataset: {e}")


def parse_html_content(html_str: str) -> Tuple[str, str]:
    """
    Extract title and main article body from HTML, stripping scripts, styles, and ads.
    Returns (page_title, clean_text).
    """
    try:
        soup = BeautifulSoup(html_str, "html.parser")

        # Extract title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        # Remove scripts, styles, navigation, footer
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        # Try to find article or main body
        article = soup.find("article") or soup.find("main") or soup.find("div", class_=["content", "article-body", "post-content"])
        if article:
            text = article.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        # Normalize redundant newlines
        cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        return (title or "Untitled Public Webpage", cleaned)
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        raise IngestionError(f"Failed to parse HTML document: {e}")


def parse_plain_text(file_bytes: bytes) -> str:
    """Safely decode plain text or markdown bytes."""
    return file_bytes.decode("utf-8", errors="replace").strip()
