#!/usr/bin/env python3
"""
Load the synthetic JSON dataset into SQLite.

Creates identities, relations, investigations, and a source record.
Safe to re-run: existing synthetic source rows are replaced.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DATASET_PATH = PROJECT_ROOT / "data" / "shadowlink_synthetic_dataset.json"

sys.path.insert(0, str(BACKEND_DIR))

from database import SessionLocal, init_db  # noqa: E402
from models.identity import Identity  # noqa: E402
from models.investigation import Investigation  # noqa: E402
from models.relation import Relation  # noqa: E402
from models.source import Source  # noqa: E402

SOURCE_NAME = "ShadowLink Synthetic Intelligence Dataset"


def load_dataset() -> dict:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. Run generate_synthetic_dataset.py first."
        )
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def replace_synthetic_rows(db) -> None:
    existing_sources = db.query(Source).filter(Source.name == SOURCE_NAME).all()
    source_ids = [s.id for s in existing_sources]
    if source_ids:
        db.query(Identity).filter(Identity.source_id.in_(source_ids)).delete(synchronize_session=False)
        db.query(Source).filter(Source.id.in_(source_ids)).delete(synchronize_session=False)
    db.query(Relation).delete()
    db.query(Investigation).delete()
    db.commit()


def main() -> int:
    init_db()
    dataset = load_dataset()
    return _write_to_db(dataset)


def _write_to_db(dataset: dict) -> int:
    db = SessionLocal()
    try:
        replace_synthetic_rows(db)

        source = Source(
            name=SOURCE_NAME,
            source_type="json",
            record_count=len(dataset["identities"]),
            extra_metadata={
                "version": dataset.get("version"),
                "classification": dataset.get("classification"),
                "purpose": dataset.get("purpose"),
            },
        )
        db.add(source)
        db.flush()

        for item in dataset["identities"]:
            db.add(
                Identity(
                    id=item["id"],
                    username=item["username"],
                    aliases=item.get("aliases", []),
                    email=item.get("email"),
                    pgp_fingerprint=item.get("pgp_fingerprint"),
                    crypto_wallets=item.get("crypto_wallets") or item.get("wallet_addresses", []),
                    platform=item.get("platform"),
                    bio=item.get("bio"),
                    writing_samples=item.get("writing_samples", []),
                    posting_hours=item.get("posting_hours") or item.get("active_hours", []),
                    categories=item.get("categories", []),
                    extra_metadata={
                        "risk_score": item.get("risk_score"),
                        "languages": item.get("languages", []),
                        "writing_style_signature": item.get("writing_style_signature", {}),
                        "posting_timestamps": item.get("posting_timestamps", []),
                        "behavioral_profile": item.get("behavioral_profile", {}),
                        "infrastructure_metadata": item.get("infrastructure_metadata", {}),
                        "cluster": (item.get("metadata") or {}).get("cluster"),
                        "synthetic": True,
                    },
                    source_id=source.id,
                )
            )

        for edge in dataset["relationships"]:
            db.add(
                Relation(
                    id=edge.get("id"),
                    source_identity_id=edge["source_identity_id"],
                    target_identity_id=edge["target_identity_id"],
                    correlation_type=edge["correlation_type"],
                    confidence_score=edge["confidence_score"],
                    evidence=edge.get("evidence", {}),
                    explanation=edge.get("explanation"),
                )
            )

        for inv in dataset["investigations"]:
            db.add(
                Investigation(
                    id=inv["id"],
                    title=inv["title"],
                    description=inv.get("description"),
                    status=inv.get("status", "open"),
                    priority=inv.get("priority", "medium"),
                    linked_identities=inv.get("linked_identity_ids") or inv.get("linked_identities", []),
                    evidence_items=inv.get("evidence_items", []),
                    notes=inv.get("notes"),
                )
            )

        db.commit()

        identity_count = db.query(Identity).count()
        relation_count = db.query(Relation).count()
        investigation_count = db.query(Investigation).count()
        source_count = db.query(Source).count()

        print(f"Loaded identities: {identity_count}")
        print(f"Loaded relations: {relation_count}")
        print(f"Loaded investigations: {investigation_count}")
        print(f"Loaded sources: {source_count}")
        print(f"SQLite database: {PROJECT_ROOT / 'data' / 'shadowlink.db'}")
        return 0
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
