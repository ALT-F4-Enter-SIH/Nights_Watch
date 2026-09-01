#!/usr/bin/env python3
"""Verify the generated synthetic dataset file without regenerating it."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "shadowlink_synthetic_dataset.json"

REQUIRED_IDENTITY_FIELDS = [
    "id",
    "username",
    "aliases",
    "writing_samples",
    "pgp_fingerprint",
    "wallet_addresses",
    "posting_timestamps",
    "active_hours",
    "languages",
    "categories",
    "risk_score",
    "relationships",
    "infrastructure_metadata",
]


def main() -> int:
    if not DATASET_PATH.exists():
        print(f"MISSING: {DATASET_PATH}")
        print("Run: python backend/seeds/generate_synthetic_dataset.py")
        return 1

    with DATASET_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)

    identities = dataset["identities"]
    edges = dataset["relationships"]
    clusters = dataset["hidden_clusters"]
    investigations = dataset["investigations"]
    stats = dataset["summary_statistics"]
    errors: list[str] = []

    if not (45 <= len(identities) <= 55):
        errors.append(f"Expected ~50 identities, got {len(identities)}")
    if len({i["username"] for i in identities}) != len(identities):
        errors.append("Duplicate usernames")
    if len(clusters) != 5:
        errors.append(f"Expected 5 clusters, got {len(clusters)}")
    if stats.get("high_confidence_edges") != 5:
        errors.append(f"High-confidence edges: {stats.get('high_confidence_edges')}")
    if stats.get("medium_confidence_edges") != 10:
        errors.append(f"Medium-confidence edges: {stats.get('medium_confidence_edges')}")
    if len(investigations) < 3:
        errors.append(f"Expected at least 3 investigations, got {len(investigations)}")

    for identity in identities:
        missing = [field for field in REQUIRED_IDENTITY_FIELDS if field not in identity]
        if missing:
            errors.append(f"{identity.get('username')}: missing {missing}")
            break

    by_name = {i["username"]: i for i in identities}
    for cluster in clusters:
        a = by_name[cluster["members"][0]]
        b = by_name[cluster["members"][1]]
        if a["pgp_fingerprint"] != b["pgp_fingerprint"]:
            errors.append(f"{cluster['name']}: PGP mismatch")
        prefix = cluster["signals"]["wallet_shared_prefix"]
        if not a["crypto_wallets"][0].startswith(prefix):
            errors.append(f"{cluster['name']}: wallet prefix mismatch")

    print(f"File: {DATASET_PATH}")
    print(f"Identities: {len(identities)}")
    print(f"Edges: {len(edges)}")
    print(f"Clusters: {len(clusters)}")
    print(f"Investigations: {len(investigations)}")
    print(f"High-confidence: {stats.get('high_confidence_edges')}")
    print(f"Medium-confidence: {stats.get('medium_confidence_edges')}")

    if errors:
        print("Verification FAILED")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Verification PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
