"""
Graph service — produces node/edge payloads for the relations graph.
"""
from __future__ import annotations

import math
from typing import List

import networkx as nx
from sqlalchemy.orm import Session

from models.identity import Identity
from models.relation import Relation


def build_graph(db: Session, *, min_confidence: float = 0.0) -> dict:
    identities = db.query(Identity).all()
    relations = (
        db.query(Relation).filter(Relation.confidence_score >= min_confidence).all()
    )

    graph = nx.Graph()
    for identity in identities:
        meta = identity.extra_metadata or {}
        risk = float(meta.get("risk_score", 0.0) or 0.0)
        graph.add_node(
            identity.id,
            username=identity.username,
            platform=identity.platform,
            risk_score=risk,
        )

    for rel in relations:
        graph.add_edge(
            rel.source_identity_id,
            rel.target_identity_id,
            correlation_type=rel.correlation_type,
            confidence_score=rel.confidence_score,
            explanation=rel.explanation,
            weight=rel.confidence_score,
        )

    nodes = [
        {
            "id": n,
            "username": graph.nodes[n]["username"],
            "platform": graph.nodes[n]["platform"],
            "risk_score": graph.nodes[n]["risk_score"],
            "degree": graph.degree(n),
        }
        for n in graph.nodes
    ]
    edges = [
        {
            "id": rel.id,
            "source": rel.source_identity_id,
            "target": rel.target_identity_id,
            "correlation_type": rel.correlation_type,
            "confidence_score": rel.confidence_score,
            "explanation": rel.explanation,
        }
        for rel in relations
    ]

    return {
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "graph_metrics": {
            "density": round(nx.density(graph), 4) if graph.number_of_nodes() else 0.0,
            "components": nx.number_connected_components(graph),
            "avg_degree": round(
                sum(dict(graph.degree()).values()) / max(1, graph.number_of_nodes()), 3
            ),
        },
    }
