#!/usr/bin/env python3
"""
ShadowLink AI — Synthetic Intelligence Dataset Generator

Generates ~50 synthetic digital identities with:
  - 5 hidden high-confidence clusters (same simulated actor)
  - ~10 medium-confidence relationship edges
  - Multiple unrelated identities
  - Seed investigations, evidence items, relationship edges,
    behavioral activity, and infrastructure metadata

All data is synthetic — defensive/educational hackathon use only.
"""
from __future__ import annotations

import json
import random
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "shadowlink_synthetic_dataset.json"
SAMPLE_IDENTITIES_PATH = PROJECT_ROOT / "data" / "samples" / "sample_identities.json"
SAMPLE_RELATIONS_PATH = PROJECT_ROOT / "data" / "samples" / "sample_relations.json"

# ---------------------------------------------------------------------------
# Hidden clusters: each pair secretly represents the same simulated actor.
# Signals: shared PGP, related wallet prefix, overlapping hours, same categories.
# ---------------------------------------------------------------------------
CLUSTERS = {
    "night_trader_cluster": {
        "members": ["NightTrader", "DarkPhoenix"],
        "pgp": "A1B2C3D4E5F67890ABCDEF1234567890ABCDEF12",
        "wallet_prefix": "0x7a2c91",
        "hours": [22, 23, 0, 1, 2],
        "categories": ["crypto_trading", "night_analysis"],
        "languages": ["en", "ru"],
        "platform": "market",
        "style": {
            "avg_word_length": 5.84,
            "punctuation_density": 0.142,
            "vocabulary_diversity": 0.81,
        },
    },
    "cyber_op_cluster": {
        "members": ["CyberWatch", "NetHunter"],
        "pgp": "B2C3D4E5F6A78901ABCDEF1234567890ABCDEF23",
        "wallet_prefix": "0x8b3d02",
        "hours": [9, 10, 11],
        "categories": ["threat_intel", "infra_scan"],
        "languages": ["en", "de"],
        "platform": "forum",
        "style": {
            "avg_word_length": 6.21,
            "punctuation_density": 0.118,
            "vocabulary_diversity": 0.88,
        },
    },
    "dark_op_cluster": {
        "members": ["GhostRunner", "ShadowDev"],
        "pgp": "C3D4E5F6A7B89012ABCDEF34567890ABCDEF3456",
        "wallet_prefix": "0x9c4e13",
        "hours": [3, 4, 5, 6],
        "categories": ["dev_sec", "exploit_research"],
        "languages": ["en", "zh"],
        "platform": "development",
        "style": {
            "avg_word_length": 5.12,
            "punctuation_density": 0.091,
            "vocabulary_diversity": 0.74,
        },
    },
    "fin_analyst_cluster": {
        "members": ["MarketEye", "TradeSense"],
        "pgp": "D4E5F6A7B8C90123ABCDEF4567890ABCDEF45678",
        "wallet_prefix": "0xad5f24",
        "hours": [14, 15, 16, 17],
        "categories": ["market_analysis", "quant_trading"],
        "languages": ["en", "es"],
        "platform": "blog",
        "style": {
            "avg_word_length": 6.55,
            "punctuation_density": 0.167,
            "vocabulary_diversity": 0.91,
        },
    },
    "security_research_cluster": {
        "members": ["InfoSecPro", "SecAnalyst"],
        "pgp": "E5F6A7B8C9D01234ABCDEF567890ABCDEF567890",
        "wallet_prefix": "0xbe6035",
        "hours": [10, 11, 12, 13],
        "categories": ["security", "vuln_research"],
        "languages": ["en", "fr"],
        "platform": "social",
        "style": {
            "avg_word_length": 5.97,
            "punctuation_density": 0.134,
            "vocabulary_diversity": 0.86,
        },
    },
}

UNRELATED = [
    "DataMiner", "CloudWalker", "SignalTracer", "PatternHunter",
    "CodeSleuth", "PacketDive", "LogDrill", "TracePath",
    "GridSearch", "NetworkScan", "DeepTrace", "CipherKey",
    "MetaScan", "DataDrift", "StreamFlow", "QueryNode",
    "LinkTrace", "PathMapper", "RouteFind", "PortScan",
    "FrameAnalyst", "PacketPro", "LogSeeker", "TraceLog",
    "SignalPulse", "WaveHunter", "DataDive", "CloudScan",
    "TraceNode", "LinkMap", "RoutePath", "PortDive",
    "FrameDeep", "NodeGraph", "SyncFlow", "ByteForge",
    "HashOrbit", "VaultIndex", "PixelTrace", "EchoGrid",
]

WRITING = {
    "crypto_trading": [
        "Market patterns indicate accumulation during off-peak hours.",
        "Wallet flow analysis shows synchronized movement across clusters.",
        "Price action correlates with hidden identity posting cycles.",
        "On-chain metrics reveal unusual transaction clustering patterns.",
        "Liquidity windows align with nocturnal observation cycles.",
    ],
    "threat_intel": [
        "Recent infrastructure scans reveal consistent fingerprint patterns.",
        "Network metadata shows overlapping origin points during active windows.",
        "Behavioral analysis indicates coordinated observation patterns.",
        "Evidence correlation points to sustained operational interest.",
        "Synthetic telemetry clustering suggests a shared observation node.",
    ],
    "security": [
        "Security assessment reveals recurring behavioral signatures.",
        "Analysis of infrastructure patterns shows consistent metadata alignment.",
        "Evidence suggests sustained monitoring activity across platforms.",
        "Defensive telemetry maps to overlapping identity windows.",
        "Control-plane observations remain within authorized research bounds.",
    ],
    "dev_sec": [
        "Development activity patterns show consistent temporal clustering.",
        "Infrastructure metadata correlates with research publication cycles.",
        "Commit windows overlap with simulated identity active hours.",
        "Build artifacts share naming conventions across aliases.",
    ],
    "market_analysis": [
        "Market behavior analysis reveals synchronized observation windows.",
        "Quantitative patterns align with specific identity clusters.",
        "Volume spikes coincide with overlapping posting hours.",
        "Cross-venue signals cluster around a shared analyst window.",
    ],
    "night_analysis": [
        "Nocturnal activity patterns reveal structured observation cycles.",
        "Off-peak analysis shows coordinated behavioral markers.",
        "Late-window telemetry remains internally consistent.",
        "Quiet-hour posting cadence matches the paired alias.",
    ],
    "vuln_research": [
        "Vulnerability patterns show consistent temporal clustering.",
        "Research publication aligns with identity activity windows.",
        "Advisory drafts share phrasing with the paired identity.",
        "Lab notes use the same synthetic citation style.",
    ],
    "exploit_research": [
        "Exploit development timelines show structured activity cycles.",
        "Research output correlates with identity behavioral markers.",
        "Proof-of-concept notes reuse a distinctive sentence cadence.",
        "Lab write-ups share punctuation density with the paired alias.",
    ],
    "infra_scan": [
        "Infrastructure scanning shows consistent temporal patterns.",
        "Network observations reveal structured behavioral cycles.",
        "Scan windows overlap with the paired identity active hours.",
        "Synthetic probe metadata shares a gateway fingerprint.",
    ],
    "quant_trading": [
        "Signal decay models cluster around a shared analyst window.",
        "Order-book observations reuse the same synthetic notation.",
        "Backtest notes share vocabulary with the paired identity.",
        "Risk commentary uses a distinctive clause rhythm.",
    ],
    "general_analysis": [
        "Synthetic identity for defensive intelligence demonstration.",
        "Simulated actor profile — authorized research dataset only.",
        "No real-world correlation is intended or implied.",
        "Behavioral markers generated for algorithm evaluation.",
        "Infrastructure metadata is fully simulated.",
    ],
    "data_review": [
        "Dataset review notes remain within authorized research bounds.",
        "Synthetic record quality checks completed without anomalies.",
        "Field completeness scores support demonstration use.",
    ],
    "pattern_recognition": [
        "Pattern recognition output is generated from mock telemetry.",
        "Cluster assignment remains a simulated research artifact.",
        "Feature vectors are synthetic and non-attributable.",
    ],
    "network_study": [
        "Network study notes describe simulated topology only.",
        "Gateway tags are mock values for demonstration.",
        "Routing metadata is generated, not observed.",
    ],
    "behavioral_analysis": [
        "Behavioral analysis uses authorized synthetic sessions.",
        "Session-length estimates are mock research values.",
        "Response latency bins are generated for scoring tests.",
    ],
    "metadata_research": [
        "Metadata research entries are fully synthetic.",
        "User-agent strings identify the research client.",
        "Origin ranges are private simulated address space.",
    ],
}

PLATFORMS = ["forum", "social", "market", "blog", "development"]
LANGUAGES = ["en", "es", "de", "fr", "ru", "zh", "ja"]
UNRELATED_CATEGORIES = [
    "general_analysis",
    "data_review",
    "pattern_recognition",
    "network_study",
    "behavioral_analysis",
    "metadata_research",
]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _pick_samples(category: str, n: int = 3) -> list[str]:
    pool = list(WRITING.get(category, WRITING["general_analysis"]))
    if len(pool) >= n:
        return random.sample(pool, n)
    extra = list(WRITING["general_analysis"])
    combined = pool + [s for s in extra if s not in pool]
    if len(combined) >= n:
        return random.sample(combined, n)
    while len(combined) < n:
        combined.append(combined[-1])
    return combined[:n]


def _wallet(prefix: str | None = None) -> str:
    if prefix:
        suffix = "".join(random.choices("0123456789abcdef", k=34))
        return f"{prefix}{suffix}"[:42]
    return "0x" + "".join(random.choices("0123456789abcdef", k=40))


def _fingerprint() -> str:
    return "".join(random.choices("0123456789ABCDEF", k=40))


def make_identity(name: str, cluster: dict | None = None, cluster_name: str | None = None) -> dict:
    """Generate a single synthetic identity with all required fields."""
    if cluster:
        cats = list(cluster["categories"])
        fp = cluster["pgp"]
        wallets = [_wallet(cluster["wallet_prefix"])]
        hours = sorted(set(cluster["hours"]))
        languages = list(cluster["languages"])
        platform = cluster["platform"]
        style = dict(cluster["style"])
        # Tiny per-identity jitter so members are similar, not identical.
        style["avg_word_length"] = round(style["avg_word_length"] + random.uniform(-0.08, 0.08), 2)
        style["punctuation_density"] = round(style["punctuation_density"] + random.uniform(-0.008, 0.008), 3)
        style["vocabulary_diversity"] = round(
            min(0.99, max(0.5, style["vocabulary_diversity"] + random.uniform(-0.02, 0.02))), 2
        )
        risk = round(random.uniform(0.62, 0.94), 2)
        origin_octet = {"night_trader_cluster": 17, "cyber_op_cluster": 34,
                        "dark_op_cluster": 51, "fin_analyst_cluster": 68,
                        "security_research_cluster": 85}.get(cluster_name or "", 10)
        infra_origin = f"192.168.{origin_octet}.{random.randint(10, 40)}"
        connection = "research_gateway"
    else:
        cats = random.sample(UNRELATED_CATEGORIES, 3)
        fp = _fingerprint()
        wallets = [_wallet()]
        hours = sorted(random.sample(range(24), 5))
        languages = random.sample(LANGUAGES, 2)
        platform = random.choice(PLATFORMS)
        style = {
            "avg_word_length": round(random.uniform(4.2, 6.8), 2),
            "punctuation_density": round(random.uniform(0.05, 0.2), 3),
            "vocabulary_diversity": round(random.uniform(0.6, 0.95), 2),
        }
        risk = round(random.uniform(0.05, 0.42), 2)
        infra_origin = f"10.{random.randint(1, 250)}.{random.randint(1, 250)}.{random.randint(1, 250)}"
        connection = random.choice(["simulated", "synthetic_proxy", "research_gateway"])

    samples = _pick_samples(cats[0], 3)
    now = _utc_now()
    timestamps = sorted(
        _iso(now - timedelta(days=random.randint(1, 45), hours=random.choice(hours), minutes=random.randint(0, 59)))
        for _ in range(random.randint(12, 28))
    )

    return {
        "id": str(uuid.uuid4()),
        "username": name,
        "aliases": [f"{name.lower()}_obs", f"{name.lower()}_{random.randint(10, 99)}"],
        "email": f"{name.lower()}@simulated.research",
        "pgp_fingerprint": fp,
        "crypto_wallets": wallets,
        "wallet_addresses": wallets,
        "platform": platform,
        "bio": "Synthetic identity — defensive intelligence demonstration.",
        "writing_samples": samples,
        "writing_style_signature": style,
        "posting_timestamps": timestamps,
        "posting_hours": hours,
        "active_hours": hours,
        "post_frequency_daily": round(random.uniform(0.5, 4.0), 2),
        "languages": languages,
        "categories": cats,
        "content_tags": cats[:2],
        "risk_score": risk,
        "relationships": [],
        "behavioral_profile": {
            "typical_session_length_minutes": random.randint(15, 120),
            "platform_switch_frequency": random.choice(["low", "medium", "high"]),
            "response_latency_pattern": random.choice(["fast", "moderate", "variable"]),
        },
        "infrastructure_metadata": {
            "origin_ip_range": infra_origin,
            "user_agent": random.choice([
                "Mozilla/5.0 (Synthetic) ShadowLink-Research/1.0",
                "Synthetic-Client/2.0 (Analysis Mode)",
            ]),
            "connection_type": connection,
            "platform_tags": random.sample(["forum", "blog", "social", "marketplace", "development"], 2),
        },
        "metadata": {
            "cluster": cluster_name,
            "synthetic": True,
            "dataset_version": "1.0.0",
        },
        "data_source": "synthetic_research_dataset",
        "dataset_version": "1.0.0",
        "created_for": "hackathon_demonstration",
        "notes": [
            "Synthetic identity — no real-world correlation intended.",
            "For defensive security research and educational purposes only.",
        ],
    }


def build_identities() -> tuple[list[dict], dict[str, str]]:
    identities: list[dict] = []
    username_to_id: dict[str, str] = {}

    for cluster_name, cluster in CLUSTERS.items():
        for member in cluster["members"]:
            identity = make_identity(member, cluster, cluster_name)
            identities.append(identity)
            username_to_id[member] = identity["id"]

    for name in UNRELATED:
        identity = make_identity(name, None, None)
        identities.append(identity)
        username_to_id[name] = identity["id"]

    return identities, username_to_id


def build_edges(identities: list[dict], username_to_id: dict[str, str]) -> list[dict]:
    edges: list[dict] = []
    by_name = {i["username"]: i for i in identities}

    for cluster_name, cluster in CLUSTERS.items():
        members = cluster["members"]
        for i, source_name in enumerate(members):
            for target_name in members[i + 1:]:
                source = by_name[source_name]
                target = by_name[target_name]
                evidence = {
                    "pgp_shared": True,
                    "pgp_fingerprint": cluster["pgp"],
                    "wallet_shared_prefix": cluster["wallet_prefix"],
                    "hours_overlap": cluster["hours"],
                    "categories_overlap": cluster["categories"],
                    "writing_style_similarity": 0.92,
                    "cluster": cluster_name,
                }
                edge = {
                    "id": str(uuid.uuid4()),
                    "source": source_name,
                    "target": target_name,
                    "source_identity_id": username_to_id[source_name],
                    "target_identity_id": username_to_id[target_name],
                    "correlation_type": "hidden_cluster",
                    "confidence_score": 0.92,
                    "evidence": evidence,
                    "evidence_items": [
                        "shared_pgp_fingerprint",
                        "related_wallet_prefix",
                        "overlapping_active_hours",
                        "matching_categories",
                        "similar_writing_style",
                    ],
                    "explanation": (
                        f"Hidden cluster — {source_name} and {target_name} share PGP fingerprint, "
                        f"related wallet prefix {cluster['wallet_prefix']}, overlapping hours "
                        f"{cluster['hours']}, and categories {cluster['categories']}. "
                        "Same simulated actor hypothesis: HIGH."
                    ),
                }
                edges.append(edge)
                source["relationships"].append({
                    "identity_id": target["id"],
                    "username": target_name,
                    "confidence_score": 0.92,
                    "correlation_type": "hidden_cluster",
                })
                target["relationships"].append({
                    "identity_id": source["id"],
                    "username": source_name,
                    "confidence_score": 0.92,
                    "correlation_type": "hidden_cluster",
                })

    cluster_members = {m for c in CLUSTERS.values() for m in c["members"]}
    unrelated_names = [i["username"] for i in identities if i["username"] not in cluster_members]
    pairs: set[tuple[str, str]] = set()
    while len(pairs) < 10:
        a, b = random.sample(unrelated_names, 2)
        pair = (min(a, b), max(a, b))
        if pair in pairs:
            continue
        pairs.add(pair)
        score = round(random.uniform(0.55, 0.75), 2)
        source = by_name[a]
        target = by_name[b]
        hours_overlap = sorted(set(source["active_hours"]).intersection(target["active_hours"]))
        cats_overlap = sorted(set(source["categories"]).intersection(target["categories"]))
        edge = {
            "id": str(uuid.uuid4()),
            "source": a,
            "target": b,
            "source_identity_id": username_to_id[a],
            "target_identity_id": username_to_id[b],
            "correlation_type": "behavioral_similarity",
            "confidence_score": score,
            "evidence": {
                "hour_overlap": hours_overlap,
                "category_overlap": cats_overlap,
                "method": "seeded_medium_confidence",
            },
            "evidence_items": ["hour_overlap", "category_overlap"],
            "explanation": (
                f"Medium-confidence behavioral correlation between {a} and {b}. "
                "Similar active windows and content categories detected in synthetic telemetry."
            ),
        }
        edges.append(edge)
        source["relationships"].append({
            "identity_id": target["id"],
            "username": b,
            "confidence_score": score,
            "correlation_type": "behavioral_similarity",
        })
        target["relationships"].append({
            "identity_id": source["id"],
            "username": a,
            "confidence_score": score,
            "correlation_type": "behavioral_similarity",
        })

    return edges


def build_investigations(username_to_id: dict[str, str]) -> list[dict]:
    now = _iso(_utc_now())
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Hidden Cluster Analysis — Night Operations",
            "description": (
                "Investigation into synchronized posting patterns between synthetic "
                "identities sharing behavioral and infrastructure markers."
            ),
            "status": "open",
            "priority": "high",
            "linked_identities": ["NightTrader", "DarkPhoenix"],
            "linked_identity_ids": [
                username_to_id["NightTrader"],
                username_to_id["DarkPhoenix"],
            ],
            "evidence_items": [
                {"type": "behavioral", "value": "Overlapping active hours (22-02)", "timestamp": now},
                {"type": "writing", "value": "Style similarity: 92%", "timestamp": now},
                {"type": "infrastructure", "value": "Related wallet prefix: 0x7a2c91", "timestamp": now},
                {"type": "pgp", "value": "Shared PGP fingerprint", "timestamp": now},
            ],
            "notes": "Synthetic research dataset — defensive intelligence demonstration only.",
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Crypto-Wallet Correlation Study",
            "description": (
                "Medium-priority analysis of related wallet activity across "
                "synthetic trading-related identities."
            ),
            "status": "open",
            "priority": "medium",
            "linked_identities": ["MarketEye", "TradeSense"],
            "linked_identity_ids": [
                username_to_id["MarketEye"],
                username_to_id["TradeSense"],
            ],
            "evidence_items": [
                {"type": "wallet", "value": "Shared wallet prefix: 0xad5f24", "timestamp": now},
                {"type": "behavioral", "value": "Active during market hours (14-17)", "timestamp": now},
            ],
            "notes": "Synthetic dataset — no real-world correlation.",
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Infrastructure Metadata Correlation",
            "description": (
                "Analysis of overlapping infrastructure fingerprints between "
                "synthetic identity pairs."
            ),
            "status": "in_review",
            "priority": "low",
            "linked_identities": ["CyberWatch", "NetHunter"],
            "linked_identity_ids": [
                username_to_id["CyberWatch"],
                username_to_id["NetHunter"],
            ],
            "evidence_items": [
                {"type": "metadata", "value": "Related PGP fingerprint segment", "timestamp": now},
                {"type": "infra", "value": "Shared research_gateway connection type", "timestamp": now},
            ],
            "notes": "Authorized synthetic data only.",
        },
    ]


def assemble_dataset() -> dict:
    identities, username_to_id = build_identities()
    edges = build_edges(identities, username_to_id)
    investigations = build_investigations(username_to_id)

    high = sum(1 for e in edges if e["confidence_score"] >= 0.85)
    medium = sum(1 for e in edges if 0.55 <= e["confidence_score"] < 0.85)

    return {
        "dataset_name": "ShadowLink AI Synthetic Intelligence Dataset",
        "version": "1.0.0",
        "generated_at": _iso(_utc_now()),
        "description": (
            "Synthetic mock dataset of digital identities with hidden clusters, "
            "behavioral correlations, and infrastructure metadata. Designed for defensive "
            "threat intelligence and educational demonstration only. No real-world data included."
        ),
        "purpose": "hackathon_demonstration_defensive_research",
        "classification": "synthetic_mock_authorized_research",
        "identities": identities,
        "relationships": edges,
        "hidden_clusters": [
            {
                "name": name,
                "members": info["members"],
                "signals": {
                    "pgp_shared": info["pgp"],
                    "wallet_shared_prefix": info["wallet_prefix"],
                    "hours_overlap": info["hours"],
                    "categories_overlap": info["categories"],
                    "languages": info["languages"],
                    "writing_style": info["style"],
                },
            }
            for name, info in CLUSTERS.items()
        ],
        "investigations": investigations,
        "summary_statistics": {
            "total_identities": len(identities),
            "total_relationship_edges": len(edges),
            "hidden_clusters": len(CLUSTERS),
            "high_confidence_edges": high,
            "medium_confidence_edges": medium,
            "unrelated_identities": len(UNRELATED),
            "investigations": len(investigations),
            "average_risk_score": round(sum(i["risk_score"] for i in identities) / len(identities), 3),
            "languages_present": sorted({lang for i in identities for lang in i["languages"]}),
            "categories_present": sorted({cat for i in identities for cat in i["categories"]}),
        },
        "disclaimer": (
            "This dataset contains ONLY synthetic, mock data. It is designed for defensive "
            "security education, authorized threat intelligence demonstration, and AI correlation "
            "algorithm testing. No real-world identities, unauthorized data, or exploitation "
            "features are included."
        ),
    }


def write_outputs(dataset: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_IDENTITIES_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    with SAMPLE_IDENTITIES_PATH.open("w", encoding="utf-8") as f:
        json.dump(dataset["identities"], f, indent=2)

    with SAMPLE_RELATIONS_PATH.open("w", encoding="utf-8") as f:
        json.dump(dataset["relationships"], f, indent=2)


def verify(dataset: dict) -> list[str]:
    errors: list[str] = []
    identities = dataset["identities"]
    edges = dataset["relationships"]
    clusters = dataset["hidden_clusters"]
    stats = dataset["summary_statistics"]

    if not (45 <= len(identities) <= 55):
        errors.append(f"Expected ~50 identities, got {len(identities)}")
    if len({i["username"] for i in identities}) != len(identities):
        errors.append("Duplicate usernames found")
    if len(clusters) != 5:
        errors.append(f"Expected 5 hidden clusters, got {len(clusters)}")
    if stats["high_confidence_edges"] != 5:
        errors.append(f"Expected 5 high-confidence edges, got {stats['high_confidence_edges']}")
    if stats["medium_confidence_edges"] != 10:
        errors.append(f"Expected 10 medium-confidence edges, got {stats['medium_confidence_edges']}")
    if len(dataset["investigations"]) != 3:
        errors.append("Expected 3 seed investigations")

    required_fields = [
        "id", "username", "aliases", "writing_samples", "pgp_fingerprint",
        "wallet_addresses", "posting_timestamps", "active_hours", "languages",
        "categories", "risk_score", "relationships", "infrastructure_metadata",
    ]
    for identity in identities:
        missing = [field for field in required_fields if field not in identity]
        if missing:
            errors.append(f"{identity.get('username')}: missing {missing}")
            break
        if len(identity["writing_samples"]) < 2:
            errors.append(f"{identity['username']}: too few writing samples")
            break

    by_name = {i["username"]: i for i in identities}
    for cluster in clusters:
        members = cluster["members"]
        if len(members) != 2:
            errors.append(f"Cluster {cluster['name']} does not have 2 members")
            continue
        a, b = by_name[members[0]], by_name[members[1]]
        if a["pgp_fingerprint"] != b["pgp_fingerprint"]:
            errors.append(f"Cluster {cluster['name']} PGP mismatch")
        if a["pgp_fingerprint"] != cluster["signals"]["pgp_shared"]:
            errors.append(f"Cluster {cluster['name']} PGP does not match declared signal")
        prefix = cluster["signals"]["wallet_shared_prefix"]
        if not a["crypto_wallets"][0].startswith(prefix) or not b["crypto_wallets"][0].startswith(prefix):
            errors.append(f"Cluster {cluster['name']} wallet prefix mismatch")
        if set(a["categories"]) != set(cluster["signals"]["categories_overlap"]):
            errors.append(f"Cluster {cluster['name']} category mismatch")

    for edge in edges:
        if not 0.0 <= edge["confidence_score"] <= 1.0:
            errors.append(f"Invalid confidence: {edge['confidence_score']}")
            break
        if edge["source_identity_id"] not in {i["id"] for i in identities}:
            errors.append(f"Dangling source id on edge {edge['id']}")
            break

    return errors


def main() -> int:
    dataset = assemble_dataset()
    write_outputs(dataset)
    errors = verify(dataset)
    stats = dataset["summary_statistics"]

    print(f"Generated {stats['total_identities']} identities")
    print(f"Generated {stats['total_relationship_edges']} relationship edges")
    print(f"Hidden clusters: {stats['hidden_clusters']}")
    print(f"High-confidence edges: {stats['high_confidence_edges']}")
    print(f"Medium-confidence edges: {stats['medium_confidence_edges']}")
    print(f"Investigations: {stats['investigations']}")
    print(f"Average risk score: {stats['average_risk_score']}")
    print(f"Saved dataset: {OUTPUT_PATH}")
    print(f"Saved samples: {SAMPLE_IDENTITIES_PATH}")
    print(f"Saved samples: {SAMPLE_RELATIONS_PATH}")

    if errors:
        print("Verification FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Verification PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
