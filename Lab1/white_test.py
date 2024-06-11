import unittest
from lab_1 import Graph

class TestCalcShortestPath(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.g = {
            'A': {'B': 1, 'C': 2},
            'B': {'C': 2, 'D': 1},
            'C': {'D': 1},
            'D': {}
        }

    def test_path_exists_word2_none(self):
        """Test when word2 is None and the graph has a path from word1 to randomly chosen word2"""
        result = self.graph.calc_shortest_path('A')
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 1)  # Ensure there is a path

    def test_path_exists_word2_specified(self):
        """Test when both word1 and word2 are specified and a path exists between them"""
        result = self.graph.calc_shortest_path('A', 'D')
        self.assertIsNotNone(result)
        expected_path = ['A', 'B', 'D']
        self.assertEqual(result, expected_path)

    def test_no_path(self):
        """Test when word1 exists but word2 does not exist in the graph (should not happen in given constraints)"""
        result = self.graph.calc_shortest_path('A', 'E')
        self.assertIsNone(result)

    def test_same_word(self):
        """Test when word1 and word2 are the same"""
        result = self.graph.calc_shortest_path('A', 'A')
        self.assertIsNotNone(result)
        expected_path = ['A']
        self.assertEqual(result, expected_path)

    def test_single_node(self):
        """Test when the graph has a single node and word1 is the same as word2"""
        single_node_graph = Graph()
        single_node_graph.g = {'A': {}}
        result = single_node_graph.calc_shortest_path('A', 'A')
        self.assertIsNotNone(result)
        expected_path = ['A']
        self.assertEqual(result, expected_path)

if __name__ == '__main__':
    unittest.main()