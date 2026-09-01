"""End-to-end test for the FastAPI backend."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from database import init_db
from main import app
from seeds.load_into_sqlite import main as load_main


@pytest.fixture(scope="module", autouse=True)
def _load_synthetic_dataset():
    init_db()
    load_main()
    yield


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_dashboard(client: TestClient) -> None:
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    body = res.json()
    assert "overview" in body
    assert body["overview"]["total_identities"] >= 40
    assert body["overview"]["total_relations"] >= 5
    assert body["overview"]["avg_confidence"] > 0


def test_list_identities(client: TestClient) -> None:
    res = client.get("/api/identities", params={"page": 1, "page_size": 5})
    assert res.status_code == 200
    body = res.json()
    assert body["page"] == 1
    assert body["page_size"] == 5
    assert body["total"] >= 40
    assert isinstance(body["data"], list) and body["data"]


def test_get_identity_by_id(client: TestClient) -> None:
    listing = client.get("/api/identities", params={"page": 1, "page_size": 1}).json()
    identity_id = listing["data"][0]["id"]
    res = client.get(f"/api/identities/{identity_id}")
    assert res.status_code == 200
    assert res.json()["id"] == identity_id


def test_get_identity_not_found(client: TestClient) -> None:
    res = client.get("/api/identities/does-not-exist")
    assert res.status_code == 404


def test_list_investigations(client: TestClient) -> None:
    res = client.get("/api/investigations")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert body
    assert all("title" in item for item in body)


def test_get_investigation(client: TestClient) -> None:
    listing = client.get("/api/investigations").json()
    investigation_id = listing[0]["id"]
    res = client.get(f"/api/investigations/{investigation_id}")
    assert res.status_code == 200
    assert res.json()["id"] == investigation_id


def test_graph(client: TestClient) -> None:
    res = client.get("/api/graph")
    assert res.status_code == 200
    body = res.json()
    assert "nodes" in body and "edges" in body
    assert body["node_count"] >= 1


def test_correlation_analyze(client: TestClient) -> None:
    identities = client.get("/api/identities", params={"page": 1, "page_size": 50}).json()["data"]
    ids = [identities[0]["id"], identities[1]["id"], identities[2]["id"]]
    res = client.post(
        "/api/correlation/analyze",
        json={"identity_ids": ids, "methods": ["username", "alias", "pgp", "wallet", "behavioral"]},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["identities_analyzed"] == 3
    assert body["pair_count"] == 3
    assert "correlations" in body
    assert isinstance(body["correlations"], list)


def test_correlation_analyze_validation(client: TestClient) -> None:
    res = client.post("/api/correlation/analyze", json={"identity_ids": ["a"]})
    assert res.status_code == 422


def test_stylometry_compare(client: TestClient) -> None:
    text_a = "Synthetic behavior shows consistent posting windows across platform X."
    text_b = "Synthetic behavior shows consistent posting windows across platform X."
    res = client.post("/api/stylometry/compare", json={"text_a": text_a, "text_b": text_b})
    assert res.status_code == 200
    body = res.json()
    assert body["similarity_score"] > 0.9
    assert body["shared_ngrams"] > 0


def test_stylometry_too_short(client: TestClient) -> None:
    res = client.post(
        "/api/stylometry/compare",
        json={"text_a": "hi", "text_b": "world"},
    )
    assert res.status_code == 422


def test_behavior(client: TestClient) -> None:
    identities = client.get("/api/identities", params={"page": 1, "page_size": 1}).json()["data"]
    identity_id = identities[0]["id"]
    res = client.get(f"/api/behavior/{identity_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["identity_id"] == identity_id
    assert "hourly_distribution" in body


def test_infrastructure_analyze(client: TestClient) -> None:
    res = client.post("/api/infrastructure/analyze", json={})
    assert res.status_code == 200
    body = res.json()
    assert body["analyzed_pairs"] >= 0
    assert isinstance(body["links"], list)


def test_infrastructure_profile(client: TestClient) -> None:
    identities = client.get("/api/identities", params={"page": 1, "page_size": 1}).json()["data"]
    identity_id = identities[0]["id"]
    res = client.get(f"/api/infrastructure/{identity_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["identity_id"] == identity_id
    assert "infrastructure_score" in body


def test_report(client: TestClient) -> None:
    listing = client.get("/api/investigations").json()
    res = client.get(f"/api/reports/{listing[0]['id']}")
    assert res.status_code == 200
    body = res.json()
    assert "sections" in body
    assert "clusters" in body
    assert body["total_correlations_found"] >= 0
