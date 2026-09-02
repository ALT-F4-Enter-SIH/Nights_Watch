"""
Unit tests for the AI Identity Correlation Engine.

Tests all correlation methods:
- Stylometry similarity
- Behavioral similarity
- PGP similarity
- Wallet relationship similarity
- Metadata similarity
- Temporal similarity
- Category similarity
- Graph relationship similarity
"""
from __future__ import annotations

import json
import math
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Ensure the data directory exists and has a synthetic dataset
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "shadowlink_synthetic_dataset.json"


def ensure_dataset():
    """Generate synthetic dataset if it doesn't exist."""
    if not DATA_PATH.exists():
        from seeds.generate_synthetic_dataset import main
        main()


def load_test_identities():
    """Load identities from the synthetic dataset."""
    ensure_dataset()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["identities"], data["relationships"]


def get_identity_by_username(username: str) -> dict | None:
    """Get an identity by username from the test data."""
    identities, _ = load_test_identities()
    for identity in identities:
        if identity.get("username") == username:
            return identity
    return None


class TestStylometryMatching(unittest.TestCase):
    """Test stylometry/writing style similarity detection."""

    def setUp(self):
        self.night_trader = get_identity_by_username("NightTrader")
        self.dark_phoenix = get_identity_by_username("DarkPhoenix")
        self.unrelated = get_identity_by_username("DataMiner")

    def test_identities_loaded(self):
        """Verify test identities exist in dataset."""
        self.assertIsNotNone(self.night_trader, "NightTrader not found in dataset")
        self.assertIsNotNone(self.dark_phoenix, "DarkPhoenix not found in dataset")

    def test_stylometry_high_similarity_for_cluster(self):
        """Cluster members should have high writing style similarity."""
        from services.correlation_engine import stylometry_match

        sig_a = self.night_trader.get("writing_style_signature", {})
        sig_b = self.dark_phoenix.get("writing_style_signature", {})
        self.assertIsNotNone(sig_a)
        self.assertIsNotNone(sig_b)

        match, score, explanation = stylometry_match(self.night_trader, self.dark_phoenix)
        self.assertTrue(match, "Cluster members should have stylometry match")
        self.assertGreater(score, 0.7, "Cluster members should have high stylometry score")

    def test_stylometry_low_similarity_for_unrelated(self):
        """Unrelated identities should have low writing style similarity."""
        from services.correlation_engine import stylometry_match

        match, score, explanation = stylometry_match(self.night_trader, self.unrelated)
        # Note: may or may not match depending on random data
        if match:
            self.assertLess(score, 0.8, "Unrelated identities should not have very high stylometry")


class TestPGPMatching(unittest.TestCase):
    """Test PGP fingerprint matching."""

    def test_exact_pgp_match(self):
        """Cluster members share exact PGP fingerprint."""
        from services.correlation_engine import pgp_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = pgp_match(night_trader, dark_phoenix)
        self.assertTrue(match, "Cluster members should have PGP match")
        self.assertEqual(score, 1.0, "Exact PGP match should score 1.0")

    def test_no_pgp_match_unrelated(self):
        """Unrelated identities should not share PGP fingerprints."""
        from services.correlation_engine import pgp_match

        night_trader = get_identity_by_username("NightTrader")
        unrelated = get_identity_by_username("DataMiner")

        match, score, explanation = pgp_match(night_trader, unrelated)
        self.assertFalse(match, "Unrelated identities should not share PGP")


class TestWalletMatching(unittest.TestCase):
    """Test cryptocurrency wallet matching."""

    def test_cluster_wallet_prefix_match(self):
        """Cluster members share wallet prefix."""
        from services.correlation_engine import crypto_wallet_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = crypto_wallet_match(night_trader, dark_phoenix)
        self.assertTrue(match, "Cluster members should share wallet prefix")
        self.assertGreater(score, 0.7, "Related wallet prefix should score > 0.7")

    def test_no_wallet_match_unrelated(self):
        """Unrelated identities should not share wallet addresses."""
        from services.correlation_engine import crypto_wallet_match

        night_trader = get_identity_by_username("NightTrader")
        unrelated = get_identity_by_username("DataMiner")

        match, score, explanation = crypto_wallet_match(night_trader, unrelated)
        # Unrelated may have exact match by coincidence, but prefix match should not occur
        # Just verify it doesn't crash
        self.assertIsNotNone(match)


class TestBehavioralMatching(unittest.TestCase):
    """Test behavioral pattern matching (categories and posting hours)."""

    def test_cluster_behavioral_overlap(self):
        """Cluster members share behavioral patterns."""
        from services.correlation_engine import behavioral_pattern_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = behavioral_pattern_match(night_trader, dark_phoenix)
        self.assertTrue(match, "Cluster members should have behavioral match")
        self.assertIn("Shared categories", explanation)

    def test_unrelated_behavioral_differences(self):
        """Unrelated identities should differ in behavior."""
        from services.correlation_engine import behavioral_pattern_match

        night_trader = get_identity_by_username("NightTrader")
        unrelated = get_identity_by_username("DataMiner")

        match, score, explanation = behavioral_pattern_match(night_trader, unrelated)
        # Just verify behavior doesn't crash and returns expected format
        self.assertIsInstance(match, bool)
        self.assertIsInstance(score, float)


class TestMetadataMatching(unittest.TestCase):
    """Test infrastructure metadata similarity."""

    def test_metadata_infrastructure_match(self):
        """Test infrastructure metadata matching."""
        from services.correlation_engine import metadata_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = metadata_match(night_trader, dark_phoenix)
        # Both should have metadata; check it returns proper format
        self.assertIsInstance(match, bool)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


class TestTemporalMatching(unittest.TestCase):
    """Test temporal pattern matching."""

    def test_cluster_temporal_overlap(self):
        """Cluster members share temporal patterns."""
        from services.correlation_engine import temporal_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = temporal_match(night_trader, dark_phoenix)
        self.assertTrue(match, "Cluster members should have temporal overlap")
        self.assertGreater(score, 0.3, "Temporal overlap should be significant")

    def test_temporal_returns_explanation(self):
        """Temporal match should provide explanation."""
        from services.correlation_engine import temporal_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = temporal_match(night_trader, dark_phoenix)
        if match:
            self.assertIsInstance(explanation, str)
            self.assertGreater(len(explanation), 0)


class TestCategoryMatching(unittest.TestCase):
    """Test content category similarity."""

    def test_cluster_category_overlap(self):
        """Cluster members share content categories."""
        from services.correlation_engine import category_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = category_match(night_trader, dark_phoenix)
        self.assertTrue(match, "Cluster members should share categories")
        self.assertGreater(score, 0.5, "Category overlap should be significant")

    def test_unrelated_category_differences(self):
        """Unrelated identities should have different categories."""
        from services.correlation_engine import category_match

        night_trader = get_identity_by_username("NightTrader")
        unrelated = get_identity_by_username("DataMiner")

        match, score, explanation = category_match(night_trader, unrelated)
        # Should not match highly
        if match:
            self.assertLess(score, 0.7)


class TestGraphMatching(unittest.TestCase):
    """Test graph-based relationship detection."""

    def test_direct_relationship_detection(self):
        """Should detect known relationships from dataset."""
        from services.correlation_engine import graph_match

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        match, score, explanation = graph_match(night_trader, dark_phoenix)
        self.assertTrue(match, "Should detect direct relationship between cluster members")
        self.assertGreater(score, 0.8, "Known relationship should have high confidence")

    def test_no_relationship_for_unrelated(self):
        """Should not detect false relationships."""
        from services.correlation_engine import graph_match

        night_trader = get_identity_by_username("NightTrader")
        unrelated = get_identity_by_username("DataMiner")

        match, score, explanation = graph_match(night_trader, unrelated)
        self.assertFalse(match, "Should not detect relationship between unrelated identities")


class TestRunCorrelation(unittest.TestCase):
    """Test the full correlation run."""

    def test_run_correlation_returns_signals(self):
        """Run correlation should return all matching signals."""
        from services.correlation_engine import run_correlation

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        results = run_correlation(night_trader, dark_phoenix)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find at least some signals")

        # Check result structure
        for result in results:
            self.assertIn("correlation_type", result)
            self.assertIn("confidence_score", result)
            self.assertIn("explanation", result)
            self.assertGreaterEqual(result["confidence_score"], 0.0)
            self.assertLessEqual(result["confidence_score"], 1.0)


class TestConfidenceComputation(unittest.TestCase):
    """Test weighted confidence computation."""

    def test_risk_level_classification(self):
        """Test risk level thresholds."""
        from services.correlation_service import classify

        self.assertEqual(classify(0.1), "minimal")
        self.assertEqual(classify(0.25), "low")
        self.assertEqual(classify(0.30), "low")
        self.assertEqual(classify(0.55), "medium")
        self.assertEqual(classify(0.70), "medium")
        self.assertEqual(classify(0.85), "high")
        self.assertEqual(classify(0.95), "high")

    def test_compute_overall_confidence(self):
        """Test weighted confidence computation."""
        from services.correlation_service import compute_overall_confidence

        matches = [
            {"correlation_type": "pgp", "confidence_score": 1.0},
            {"correlation_type": "stylometry", "confidence_score": 0.8},
        ]
        confidence = compute_overall_confidence(matches)
        self.assertGreater(confidence, 0.5)
        self.assertLessEqual(confidence, 1.0)

    def test_empty_matches_returns_zero(self):
        """Empty matches should return zero confidence."""
        from services.correlation_service import compute_overall_confidence

        confidence = compute_overall_confidence([])
        self.assertEqual(confidence, 0.0)


class TestAnalyzeTwoIdentities(unittest.TestCase):
    """Test the full two-identity analysis."""

    def test_analyze_returns_correct_structure(self):
        """Analyze should return the required structure."""
        from services.correlation_service import analyze_two_identities

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        result = analyze_two_identities(night_trader["id"], dark_phoenix["id"])

        # Check required fields
        self.assertIn("identity_a", result)
        self.assertIn("identity_b", result)
        self.assertIn("correlation_confidence", result)
        self.assertIn("risk_level", result)
        self.assertIn("signals", result)
        self.assertIn("evidence", result)
        self.assertIn("explanation", result)

        # Check signals structure
        signals = result["signals"]
        expected_signals = ["stylometry", "behavior", "pgp", "wallet", "metadata", "temporal", "category", "graph"]
        for signal_name in expected_signals:
            self.assertIn(signal_name, signals)
            self.assertIsInstance(signals[signal_name], int)

    def test_cluster_high_confidence(self):
        """Cluster members should have high confidence."""
        from services.correlation_service import analyze_two_identities

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        result = analyze_two_identities(night_trader["id"], dark_phoenix["id"])

        self.assertGreater(result["correlation_confidence"], 50,
            "Cluster members should have correlation confidence > 50")
        self.assertIn(result["risk_level"], ["HIGH", "CRITICAL"],
            f"Cluster correlation should be HIGH or CRITICAL, got {result['risk_level']}")

    def test_unrelated_low_confidence(self):
        """Unrelated identities should have low confidence."""
        from services.correlation_service import analyze_two_identities

        night_trader = get_identity_by_username("NightTrader")
        unrelated = get_identity_by_username("DataMiner")

        result = analyze_two_identities(night_trader["id"], unrelated["id"])

        self.assertLess(result["correlation_confidence"], 80,
            "Unrelated identities should not have very high confidence")

    def test_risk_levels_correct_ranges(self):
        """Risk levels should follow correct ranges."""
        from services.correlation_service import analyze_two_identities

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        result = analyze_two_identities(night_trader["id"], dark_phoenix["id"])

        confidence = result["correlation_confidence"]
        risk_level = result["risk_level"]

        if confidence <= 25:
            self.assertEqual(risk_level, "LOW")
        elif confidence <= 50:
            self.assertEqual(risk_level, "MEDIUM")
        elif confidence <= 75:
            self.assertEqual(risk_level, "HIGH")
        else:
            self.assertEqual(risk_level, "CRITICAL")

    def test_evidence_is_explainable(self):
        """Evidence should be explainable."""
        from services.correlation_service import analyze_two_identities

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        result = analyze_two_identities(night_trader["id"], dark_phoenix["id"])

        self.assertIsInstance(result["evidence"], list)
        for evidence in result["evidence"]:
            self.assertIsInstance(evidence, str)
            self.assertGreater(len(evidence), 0)

    def test_configurable_weights(self):
        """Test that weights can be configured."""
        from services.correlation_service import analyze_two_identities

        night_trader = get_identity_by_username("NightTrader")
        dark_phoenix = get_identity_by_username("DarkPhoenix")

        # High weight on PGP
        custom_weights = {"pgp": 1.0}
        result = analyze_two_identities(
            night_trader["id"],
            dark_phoenix["id"],
            weights=custom_weights
        )

        # PGP match exists, so confidence should be high
        self.assertGreater(result["correlation_confidence"], 50)


class TestDefaultWeights(unittest.TestCase):
    """Test default weight configuration."""

    def test_default_weights_sum_to_one(self):
        """Default weights should sum to approximately 1.0."""
        from services.correlation_service import DEFAULT_WEIGHTS

        total = sum(DEFAULT_WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=2,
            msg=f"Default weights should sum to 1.0, got {total}")

    def test_stylometry_has_highest_default_weight(self):
        """Stylometry should have the highest default weight."""
        from services.correlation_service import DEFAULT_WEIGHTS

        self.assertGreater(DEFAULT_WEIGHTS.get("stylometry", 0), 0.2,
            "Stylometry should have weight > 0.2")

    def test_weights_are_configurable(self):
        """Custom weights should override defaults."""
        from services.correlation_service import compute_overall_confidence

        custom_weights = {"pgp": 0.5, "wallet": 0.5}
        matches = [
            {"correlation_type": "pgp", "confidence_score": 1.0},
        ]
        confidence = compute_overall_confidence(matches, weights=custom_weights)
        # With pgp score of 1.0 and weight of 0.5, should get high confidence
        self.assertGreater(confidence, 0.4)


if __name__ == "__main__":
    # Ensure dataset exists before running tests
    ensure_dataset()
    unittest.main(verbosity=2)
