"""Tests for Phase 7: Graph Intelligence Engine."""
import sys, unittest
sys.path.insert(0, '.')
from backend.services import graph_service

class Phase7GraphTests(unittest.TestCase):
    def test_graph_build(self):
        g = graph_service.build_graph()
        self.assertIn('nodes', g)
        self.assertIn('edges', g)
        self.assertIn('metrics', g)
        self.assertGreaterEqual(g['metrics']['node_count'], 3)

    def test_connected_entities(self):
        G = graph_service._build_multimodal_graph()
        entities = graph_service.find_connected_entities(G, G.nodes()[0], depth=2)
        self.assertGreater(len(entities), 0)

    def test_strongest_relationships(self):
        G = graph_service._build_multimodal_graph()
        rels = graph_service.find_strongest_relationships(G, top_k=5)
        self.assertIsInstance(rels, list)

    def test_clusters(self):
        clusters = graph_service.get_graph_algorithms()['clusters']
        self.assertIsInstance(clusters, list)

if __name__ == '__main__':
    unittest.main()
