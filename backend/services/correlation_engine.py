"""Identity correlation engine — signal extraction and scoring for identity pairs."""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import json
import math


def exact_username_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for exact username match between two identities."""
    if id1.get("username") == id2.get("username"):
        return True, 1.0, "Exact username match"
    return False, 0.0, ""


def fuzzy_alias_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for alias overlap using exact and substring matching."""
    aliases1 = set(str(a).lower() for a in id1.get("aliases", []))
    aliases2 = set(str(a).lower() for a in id2.get("aliases", []))
    common = aliases1.intersection(aliases2)
    if common:
        score = min(0.95, 0.5 + 0.2 * len(common))
        return True, score, f"Shared aliases: {', '.join(common)}"
    for a1 in aliases1:
        for a2 in aliases2:
            if a1 in a2 or a2 in a1:
                return True, 0.75, f"Similar alias: {a1} / {a2}"
    return False, 0.0, ""


def pgp_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for PGP fingerprint match."""
    fp1 = id1.get("pgp_fingerprint") or ""
    fp2 = id2.get("pgp_fingerprint") or ""
    if fp1 and fp2 and fp1 == fp2:
        return True, 1.0, "Exact PGP fingerprint match"
    if fp1 and fp2:
        fp1_short = fp1[-16:] if len(fp1) >= 16 else fp1
        fp2_short = fp2[-16:] if len(fp2) >= 16 else fp2
        if fp1_short == fp2_short:
            return True, 0.85, "PGP short key ID match"
    return False, 0.0, ""


def crypto_wallet_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for crypto wallet overlap."""
    w1 = set(str(w).lower() for w in id1.get("crypto_wallets", []))
    w2 = set(str(w).lower() for w in id2.get("crypto_wallets", []))
    common = w1.intersection(w2)
    if common:
        return True, 1.0, f"Shared wallet: {', '.join(common)}"
    # Check for related wallet prefixes
    if w1 and w2:
        for wallet1 in w1:
            for wallet2 in w2:
                if len(wallet1) >= 8 and len(wallet2) >= 8:
                    if wallet1[:8] == wallet2[:8]:
                        return True, 0.75, f"Related wallet prefix detected: {wallet1[:10]}... / {wallet2[:10]}..."
    return False, 0.0, ""


def behavioral_pattern_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for behavioral pattern overlap (categories and posting hours)."""
    cats1 = set(str(c).lower() for c in id1.get("categories", []))
    cats2 = set(str(c).lower() for c in id2.get("categories", []))
    common_cats = cats1.intersection(cats2)
    hours1 = set(id1.get("posting_hours", []))
    hours2 = set(id2.get("posting_hours", []))
    common_hours = hours1.intersection(hours2)
    score = 0.0
    evidence = []
    if common_cats:
        score += 0.4 + 0.1 * len(common_cats)
        evidence.append(f"Shared categories: {', '.join(common_cats)}")
    if common_hours:
        hour_score = len(common_hours) / max(len(hours1), len(hours2), 1)
        score += 0.4 * hour_score
        evidence.append(f"Shared posting hours: {len(common_hours)}")
    return score > 0, min(0.8, score), "; ".join(evidence) if evidence else ""


def stylometry_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for writing style similarity using stored signatures."""
    sig1 = id1.get("writing_style_signature", {}) or {}
    sig2 = id2.get("writing_style_signature", {}) or {}
    if not sig1 or not sig2:
        return False, 0.0, "No writing style signatures available"

    score = 0.0
    comparisons = 0
    if "avg_word_length" in sig1 and "avg_word_length" in sig2:
        diff = abs(sig1["avg_word_length"] - sig2["avg_word_length"])
        score += max(0, 1 - diff / 2.0)
        comparisons += 1
    if "punctuation_density" in sig1 and "punctuation_density" in sig2:
        diff = abs(sig1["punctuation_density"] - sig2["punctuation_density"])
        score += max(0, 1 - diff / 0.2)
        comparisons += 1
    if "vocabulary_diversity" in sig1 and "vocabulary_diversity" in sig2:
        diff = abs(sig1["vocabulary_diversity"] - sig2["vocabulary_diversity"])
        score += max(0, 1 - diff / 0.5)
        comparisons += 1

    if comparisons == 0:
        return False, 0.0, "No comparable style features"
    final_score = score / comparisons
    if final_score >= 0.75:
        return True, final_score, f"High writing style similarity: {final_score:.1%}"
    elif final_score >= 0.6:
        return True, final_score, f"Moderate writing style similarity: {final_score:.1%}"
    return False, 0.0, ""


def metadata_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for metadata similarity (languages, infrastructure, etc.)."""
    meta1 = id1.get("infrastructure_metadata", {}) or {}
    meta2 = id2.get("infrastructure_metadata", {}) or {}
    score = 0.0
    shared = []

    # Check shared infrastructure metadata
    if meta1.get("origin_ip_range") and meta1.get("origin_ip_range") == meta2.get("origin_ip_range"):
        shared.append("origin_ip_range")
        score += 0.35
    if meta1.get("connection_type") and meta1.get("connection_type") == meta2.get("connection_type"):
        shared.append("connection_type")
        score += 0.2
    if meta1.get("user_agent") and meta1.get("user_agent") == meta2.get("user_agent"):
        shared.append("user_agent")
        score += 0.35
    if meta1.get("platform_tags") and meta2.get("platform_tags"):
        common_tags = set(meta1["platform_tags"]) & set(meta2["platform_tags"])
        if common_tags:
            shared.append(f"platform_tags:{len(common_tags)}")
            score += 0.1 * len(common_tags)

    # Check language overlap
    lang1 = set(id1.get("languages", []))
    lang2 = set(id2.get("languages", []))
    common_langs = lang1 & lang2
    if common_langs:
        shared.append(f"languages:{','.join(common_langs)}")
        score += 0.15

    if not shared:
        return False, 0.0, ""
    return True, min(1.0, score), f"Metadata similarity: {', '.join(shared)}"


def temporal_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for temporal (time-based) similarity in posting patterns."""
    hours1 = set(id1.get("posting_hours", []))
    hours2 = set(id2.get("posting_hours", []))
    timestamps1 = id1.get("posting_timestamps", [])
    timestamps2 = id2.get("posting_timestamps", [])

    score = 0.0
    evidence = []

    # Hour overlap score
    if hours1 and hours2:
        intersection = hours1 & hours2
        union = hours1 | hours2
        if union:
            jaccard = len(intersection) / len(union)
            score += jaccard * 0.5
            if intersection:
                evidence.append(f"Hour overlap: {sorted(intersection)}")

    # Timestamp clustering analysis
    if timestamps1 and timestamps2:
        try:
            ts1_dates = [datetime.fromisoformat(t.replace("Z", "+00:00")) for t in timestamps1[:5]]
            ts2_dates = [datetime.fromisoformat(t.replace("Z", "+00:00")) for t in timestamps2[:5]]
            if ts1_dates and ts2_dates:
                avg_diff_hours = 0
                for t1 in ts1_dates[:3]:
                    min_diff = min(abs((t1 - t2).total_seconds() / 3600) for t2 in ts2_dates[:3])
                    avg_diff_hours += min_diff
                avg_diff_hours /= min(3, len(ts1_dates))
                if avg_diff_hours < 2:
                    score += 0.5
                    evidence.append(f"Close temporal clustering: avg {avg_diff_hours:.1f}h apart")
                elif avg_diff_hours < 6:
                    score += 0.25
                    evidence.append(f"Similar posting windows: avg {avg_diff_hours:.1f}h apart")
        except (ValueError, TypeError):
            pass

    if score > 0:
        return True, min(1.0, score), "; ".join(evidence)
    return False, 0.0, ""


def category_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for content category similarity."""
    cats1 = set(str(c).lower() for c in id1.get("categories", []))
    cats2 = set(str(c).lower() for c in id2.get("categories", []))

    if not cats1 or not cats2:
        return False, 0.0, ""

    intersection = cats1 & cats2
    union = cats1 | cats2
    jaccard = len(intersection) / len(union) if union else 0.0

    if jaccard >= 0.5:
        return True, jaccard, f"High category overlap: {len(intersection)} shared of {len(union)} total"
    elif jaccard >= 0.25:
        return True, jaccard, f"Moderate category overlap: {', '.join(intersection)}"
    return False, 0.0, ""


def _load_dataset() -> Tuple[List[Dict], List[Dict]]:
    """Load the synthetic dataset for graph-based correlation."""
    DATASET_PATH = Path(__file__).parent.parent.parent / "data" / "shadowlink_synthetic_dataset.json"
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["identities"], data["relationships"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return [], []


def graph_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    """Check for graph-based relationship (known relationships from dataset)."""
    identities, relationships = _load_dataset()

    id1_lookup = next((i for i in identities if i["id"] == id1.get("id")), None)
    id2_lookup = next((i for i in identities if i["id"] == id2.get("id")), None)

    if not id1_lookup or not id2_lookup:
        return False, 0.0, "Identities not found in dataset"

    # Check direct relationships
    for rel in relationships:
        if (rel["source_identity_id"] == id1.get("id") and rel["target_identity_id"] == id2.get("id")) or \
           (rel["source_identity_id"] == id2.get("id") and rel["target_identity_id"] == id1.get("id")):
            return True, rel["confidence_score"], (
                f"Known relationship found: {rel.get('correlation_type', 'direct')} "
                f"(confidence: {rel['confidence_score']:.2f})"
            )

    # Check shared third-party connections
    id1_rels = set()
    id2_rels = set()
    for rel in relationships:
        if rel["source_identity_id"] == id1.get("id"):
            id1_rels.add(rel["target_identity_id"])
        elif rel["target_identity_id"] == id1.get("id"):
            id1_rels.add(rel["source_identity_id"])
        if rel["source_identity_id"] == id2.get("id"):
            id2_rels.add(rel["target_identity_id"])
        elif rel["target_identity_id"] == id2.get("id"):
            id2_rels.add(rel["source_identity_id"])

    shared_connections = id1_rels & id2_rels
    if shared_connections:
        return True, 0.4, f"Shared connections with {len(shared_connections)} third-party identity(ies)"

    return False, 0.0, "No graph-based relationship detected"


def run_correlation(id1: Dict, id2: Dict) -> List[Dict]:
    """Run all correlation methods on a pair of identities."""
    relations = []
    for fn, label in [
        (exact_username_match, "username"),
        (fuzzy_alias_match, "alias"),
        (pgp_match, "pgp"),
        (crypto_wallet_match, "crypto"),
        (behavioral_pattern_match, "behavioral"),
        (stylometry_match, "stylometry"),
        (metadata_match, "metadata"),
        (temporal_match, "temporal"),
        (category_match, "category"),
        (graph_match, "graph"),
    ]:
        match, score, explanation = fn(id1, id2)
        if match:
            relations.append({
                "correlation_type": label,
                "confidence_score": score,
                "evidence": {"method": label},
                "explanation": explanation,
            })
    return relations
