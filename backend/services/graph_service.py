"""
Graph service — produces node/edge payloads for the relations graph.

Phase 7: Graph Intelligence Engine
Builds a multi-modal graph with:
- Node types: Identity, Alias, PGP Key, Wallet, Writing Profile, Behavioral Cluster, Infrastructure Indicator
- Edge types: Shared PGP, Shared Wallet, Stylometric Similarity, Behavioral Similarity, Metadata Similarity, Reputation
- Each edge carries: relationship_type, confidence, evidence, weight
- Implements: connected entities, strongest relationships, shortest path, cluster detection, centrality
"""
from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional, Any
import json

import networkx as nx
from sqlalchemy.orm import Session

from models.identity import Identity
from models.relation import Relation

# Path to synthetic dataset
DATASET_PATH = Path(__file__).parent.parent.parent / "data" / "shadowlink_synthetic_dataset.json"


def _load_dataset() -> tuple[list[dict], list[dict]]:
    """Load synthetic dataset identities and relationships."""
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("identities", []), data.get("relationships", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return [], []


def _node_kind(node_type: str) -> str:
    """Map internal type to a frontend-friendly kind label."""
    mapping = {
        "identity": "Identity",
        "alias": "Alias",
        "pgp": "PGPKey",
        "wallet": "Wallet",
        "writing": "WritingProfile",
        "behavioral_cluster": "BehavioralCluster",
        "infrastructure": "InfrastructureIndicator",
    }
    return mapping.get(node_type, node_type)


def _build_multimodal_graph() -> nx.Graph:
    """Build a multi-modal graph from synthetic dataset identities and relationships."""
    identities, relationships = _load_dataset()
    G = nx.Graph()

    for identity in identities:
        uid = identity["id"]
        username = identity.get("username", "")
        G.add_node(
            f"identity:{uid}",
            kind="identity",
            label=username,
            platform=identity.get("platform", ""),
            risk_score=identity.get("risk_score", 0.0),
        )

        # Alias nodes
        for alias in identity.get("aliases", []):
            alias_id = f"alias:{alias}"
            G.add_node(alias_id, kind="alias", label=alias, identity_id=uid)
            G.add_edge(
                f"identity:{uid}",
                alias_id,
                relationship_type="has_alias",
                confidence=1.0,
                evidence={"alias": alias},
                weight=0.3,
            )

        # PGP key node
        pgp = identity.get("pgp_fingerprint")
        if pgp:
            pgp_id = f"pgp:{pgp}"
            G.add_node(pgp_id, kind="pgp", label=pgp[:16] + "...", fingerprint=pgp)
            G.add_edge(
                f"identity:{uid}",
                pgp_id,
                relationship_type="uses_pgp",
                confidence=1.0,
                evidence={"fingerprint": pgp},
                weight=0.4,
            )

        # Wallet nodes
        for wallet in identity.get("crypto_wallets", []):
            wallet_id = f"wallet:{wallet}"
            G.add_node(wallet_id, kind="wallet", label=wallet[:10] + "...", address=wallet)
            G.add_edge(
                f"identity:{uid}",
                wallet_id,
                relationship_type="owns_wallet",
                confidence=1.0,
                evidence={"wallet": wallet},
                weight=0.4,
            )

        # Writing profile node
        sig = identity.get("writing_style_signature", {}) or {}
        if sig:
            wp_id = f"writing:{uid}"
            G.add_node(
                wp_id,
                kind="writing",
                label=f"Style of {username}",
                avg_word_length=sig.get("avg_word_length", 0),
                vocabulary_diversity=sig.get("vocabulary_diversity", 0),
                punctuation_density=sig.get("punctuation_density", 0),
            )
            G.add_edge(
                f"identity:{uid}",
                wp_id,
                relationship_type="has_writing_profile",
                confidence=1.0,
                evidence={},
                weight=0.2,
            )

        # Behavioral cluster node
        categories = identity.get("categories", [])
        if categories:
            cluster_label = "+".join(sorted(categories[:2]))
            cluster_id = f"behavioral_cluster:{cluster_label}"
            G.add_node(
                cluster_id,
                kind="behavioral_cluster",
                label=cluster_label,
                categories=categories,
            )
            G.add_edge(
                f"identity:{uid}",
                cluster_id,
                relationship_type="belongs_to_cluster",
                confidence=1.0,
                evidence={"categories": categories},
                weight=0.3,
            )

        # Infrastructure indicator node
        infra = identity.get("infrastructure_metadata", {}) or {}
        if infra:
            ip_range = infra.get("origin_ip_range", "")
            if ip_range:
                inf_id = f"infrastructure:{ip_range}"
                G.add_node(
                    inf_id,
                    kind="infrastructure",
                    label=ip_range,
                    origin_ip_range=ip_range,
                    connection_type=infra.get("connection_type", ""),
                )
                G.add_edge(
                    f"identity:{uid}",
                    inf_id,
                    relationship_type="uses_infrastructure",
                    confidence=1.0,
                    evidence={"origin_ip_range": ip_range},
                    weight=0.5,
                )

    # Build cross-identity relationships from dataset relationships
    for rel in relationships:
        src = f"identity:{rel['source_identity_id']}"
        tgt = f"identity:{rel['target_identity_id']}"
        if src in G and tgt in G:
            rtype = rel.get("correlation_type", "related")
            # Map dataset relationship type to a graph relationship_type label
            if rtype == "hidden_cluster":
                graph_rel = "shared_pgp_or_wallet"
            else:
                graph_rel = "behavioral_similarity"
            G.add_edge(
                src,
                tgt,
                relationship_type=graph_rel,
                confidence=rel.get("confidence_score", 0.5),
                evidence=rel.get("evidence", {}),
                weight=rel.get("confidence_score", 0.5),
            )

    # Detect stylometric and metadata similarity edges from writing signatures
    _add_stylometric_edges(G, identities)
    _add_metadata_edges(G, identities)

    # Add reputation edges: high-risk identity → low-risk identity (no real evidence,
    # but a defensive graph hypothesis for visualization)
    _add_reputation_edges(G, identities)

    return G


def _add_stylometric_edges(G: nx.Graph, identities: list[dict]) -> None:
    """Add stylometric similarity edges between identities with similar writing."""
    sigs = {i["id"]: i.get("writing_style_signature", {}) or {} for i in identities}
    keys = list(sigs.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = sigs[keys[i]], sigs[keys[j]]
            if not a or not b:
                continue
            diff = (
                abs(a.get("avg_word_length", 0) - b.get("avg_word_length", 0)) / 6.0
                + abs(a.get("punctuation_density", 0) - b.get("punctuation_density", 0)) / 0.2
                + abs(a.get("vocabulary_diversity", 0) - b.get("vocabulary_diversity", 0))
            )
            score = max(0.0, 1.0 - diff / 3.0)
            if score >= 0.85:
                G.add_edge(
                    f"identity:{keys[i]}",
                    f"identity:{keys[j]}",
                    relationship_type="stylometric_similarity",
                    confidence=round(score, 4),
                    evidence={"method": "writing_style_features"},
                    weight=round(score, 4),
                )


def _add_metadata_edges(G: nx.Graph, identities: list[dict]) -> None:
    """Add metadata similarity edges for shared infrastructure attributes."""
    by_ip = defaultdict(list)
    by_conn = defaultdict(list)
    for i in identities:
        meta = i.get("infrastructure_metadata", {}) or {}
        ip = meta.get("origin_ip_range")
        if ip:
            by_ip[ip].append(i["id"])
        conn = meta.get("connection_type")
        if conn:
            by_conn[conn].append(i["id"])
    for ip, ids in by_ip.items():
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                G.add_edge(
                    f"identity:{ids[i]}",
                    f"identity:{ids[j]}",
                    relationship_type="metadata_similarity",
                    confidence=0.6,
                    evidence={"shared_origin_ip_range": ip},
                    weight=0.6,
                )
    for conn, ids in by_conn.items():
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                # Only add if not already in graph
                if not G.has_edge(f"identity:{ids[i]}", f"identity:{ids[j]}"):
                    G.add_edge(
                        f"identity:{ids[i]}",
                        f"identity:{ids[j]}",
                        relationship_type="metadata_similarity",
                        confidence=0.4,
                        evidence={"shared_connection_type": conn},
                        weight=0.4,
                    )


def _add_reputation_edges(G: nx.Graph, identities: list[dict]) -> None:
    """Add weak reputation-style edges (high-risk ↔ related low-risk) for graph theory demos."""
    high_risk = [i for i in identities if i.get("risk_score", 0) >= 0.8]
    low_risk = [i for i in identities if i.get("risk_score", 0) < 0.3]
    for h in high_risk:
        for l in low_risk[:2]:
            G.add_edge(
                f"identity:{h['id']}",
                f"identity:{l['id']}",
                relationship_type="reputation_relationship",
                confidence=0.2,
                evidence={"note": "weak association, defensive hypothesis only"},
                weight=0.2,
            )


def _to_cytoscape_payload(G: nx.Graph) -> dict:
    """Convert NetworkX graph to a Cytoscape / React Flow friendly payload."""
    nodes = []
    for n, attrs in G.nodes(data=True):
        nodes.append({
            "id": n,
            "label": attrs.get("label", n),
            "kind": _node_kind(attrs.get("kind", "identity")),
            "data": {k: v for k, v in attrs.items() if k not in ("label", "kind")},
        })

    edges = []
    for idx, (u, v, attrs) in enumerate(G.edges(data=True)):
        edges.append({
            "id": f"e{idx}",
            "source": u,
            "target": v,
            "relationship_type": attrs.get("relationship_type", ""),
            "confidence": attrs.get("confidence", 0.0),
            "evidence": attrs.get("evidence", {}),
            "weight": attrs.get("weight", attrs.get("confidence", 0.0)),
        })
    return {"nodes": nodes, "edges": edges}


# ---------------------------------------------------------------------------
# Graph algorithms
# ---------------------------------------------------------------------------

def find_connected_entities(G: nx.Graph, node_id: str, depth: int = 2) -> list[str]:
    """Return all entities connected to node_id up to `depth` hops."""
    if node_id not in G:
        return []
    visited = {node_id}
    frontier = {node_id}
    for _ in range(depth):
        next_frontier = set()
        for n in frontier:
            for nbr in G.neighbors(n):
                if nbr not in visited:
                    visited.add(nbr)
                    next_frontier.add(nbr)
        frontier = next_frontier
        if not frontier:
            break
    return sorted(visited)


def find_strongest_relationships(G: nx.Graph, top_k: int = 10) -> list[dict]:
    """Return the top-k strongest edges by confidence/weight."""
    edges = []
    for u, v, attrs in G.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "relationship_type": attrs.get("relationship_type", ""),
            "confidence": attrs.get("confidence", 0.0),
            "weight": attrs.get("weight", 0.0),
        })
    edges.sort(key=lambda e: e["weight"], reverse=True)
    return edges[:top_k]


def find_shortest_path(G: nx.Graph, source: str, target: str) -> Optional[list[str]]:
    """Find shortest path between two identity nodes. Returns path or None."""
    if source not in G or target not in G:
        return None
    try:
        return list(nx.shortest_path(G, source=source, target=target))
    except nx.NetworkXNoPath:
        return None


def detect_clusters(G: nx.Graph) -> list[list[str]]:
    """Detect clusters using connected components as a baseline."""
    return [sorted(list(c)) for c in nx.connected_components(G)]


def calculate_centrality(G: nx.Graph, top_k: int = 10) -> list[dict]:
    """Calculate degree and betweenness centrality for the top-k nodes."""
    if G.number_of_nodes() == 0:
        return []
    degree_cent = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    combined = []
    for n in G.nodes():
        combined.append({
            "node": n,
            "label": G.nodes[n].get("label", n),
            "degree_centrality": round(degree_cent.get(n, 0.0), 4),
            "betweenness_centrality": round(betweenness.get(n, 0.0), 4),
        })
    combined.sort(key=lambda x: (x["betweenness_centrality"], x["degree_centrality"]), reverse=True)
    return combined[:top_k]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_graph(db: Optional[Session] = None, *, min_confidence: float = 0.0) -> dict:
    """Build a frontend-friendly graph payload.

    Tries the DB first for live relations; falls back to the synthetic dataset
    so the graph is always populated for Phase 7 demo purposes.
    """
    G = _build_multimodal_graph()

    # Augment with DB-stored relations (if any)
    if db is not None:
        relations = (
            db.query(Relation)
            .filter(Relation.confidence_score >= min_confidence)
            .all()
        )
        for rel in relations:
            src = f"identity:{rel.source_identity_id}"
            tgt = f"identity:{rel.target_identity_id}"
            if src in G.nodes and tgt in G.nodes and not G.has_edge(src, tgt):
                G.add_edge(
                    src,
                    tgt,
                    relationship_type=rel.correlation_type,
                    confidence=rel.confidence_score,
                    evidence=rel.evidence or {},
                    weight=rel.confidence_score,
                )

    payload = _to_cytoscape_payload(G)
    # Trim edges below threshold
    if min_confidence > 0:
        payload["edges"] = [e for e in payload["edges"] if e.get("confidence", 0) >= min_confidence]
        used = set()
        for e in payload["edges"]:
            used.add(e["source"])
            used.add(e["target"])
        payload["nodes"] = [n for n in payload["nodes"] if n["id"] in used]

    # Metrics
    metrics = {
        "node_count": len(payload["nodes"]),
        "edge_count": len(payload["edges"]),
        "density": round(nx.density(G), 4) if G.number_of_nodes() else 0.0,
        "components": nx.number_connected_components(G),
    }

    return {
        **payload,
        "metrics": metrics,
        "strongest_relationships": find_strongest_relationships(G, top_k=10),
        "clusters": detect_clusters(G),
        "centrality": calculate_centrality(G, top_k=10),
    }


def get_graph_algorithms(db: Optional[Session] = None) -> dict:
    """Expose all graph algorithms in a single payload for testing."""
    G = _build_multimodal_graph()
    identities = [n for n, attrs in G.nodes(data=True) if attrs.get("kind") == "identity"]
    sample_source = identities[0] if identities else None
    sample_target = identities[1] if len(identities) > 1 else None
    shortest = (
        find_shortest_path(G, sample_source, sample_target)
        if sample_source and sample_target
        else None
    )
    return {
        "connected_entities": {
            sample_source: find_connected_entities(G, sample_source, depth=2)
        } if sample_source else {},
        "shortest_path": {
            "source": sample_source,
            "target": sample_target,
            "path": shortest,
        },
        "clusters": detect_clusters(G),
        "centrality_top": calculate_centrality(G, top_k=10),
    }
