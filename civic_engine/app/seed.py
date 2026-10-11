"""Seed script to populate database with realistic synthetic demonstration dataset."""

import json
import logging
import os
import sys
from datetime import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, init_db
from app.ingestion.service import IngestionService
from app.workers.pipeline import run_full_pipeline_for_source

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed")


def seed_synthetic_data(limit: int = 32, execute_pipeline: bool = True):
    """Load synthetic demonstration records from JSON and ingest into database."""
    init_db()
    db = SessionLocal()

    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample", "synthetic_sources.json")
    if not os.path.exists(json_path):
        logger.error(f"Sample data file not found at {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    logger.info(f"Loaded {len(records)} synthetic demonstration source records.")
    ingestion = IngestionService(db)
    ingested_sources = []

    for item in records[:limit]:
        pub_date = None
        if item.get("publication_date"):
            try:
                pub_date = datetime.fromisoformat(item["publication_date"].replace("Z", "+00:00"))
            except Exception:
                pass

        src = ingestion.ingest_text(
            title=item["title"],
            text=item["text"],
            publisher=item.get("publisher", "Synthetic Demonstration Dataset"),
            metadata={
                "source_type": item.get("source_type", "user_text"),
                "original_url": item.get("original_url"),
                "publication_date": item.get("publication_date"),
                "is_synthetic_demonstration": True,
            }
        )
        ingested_sources.append(src)

    logger.info(f"Successfully ingested {len(ingested_sources)} unique synthetic sources into database.")

    if execute_pipeline:
        logger.info("Executing end-to-end intelligence and extraction pipeline on ingested sources...")
        processed_count = 0
        for src in ingested_sources:
            try:
                run_full_pipeline_for_source(source_id=src.id)
                processed_count += 1
            except Exception as e:
                logger.error(f"Pipeline error for source {src.id}: {e}")

        logger.info(f"Pipeline execution finished. Processed {processed_count}/{len(ingested_sources)} sources.")

    db.close()


if __name__ == "__main__":
    limit_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    seed_synthetic_data(limit=limit_arg, execute_pipeline=True)
