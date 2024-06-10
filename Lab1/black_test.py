import unittest
import sys
from io import StringIO
from lab_1 import Graph

class TestQueryBridgeWords(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.g = {
            "apple": {"banana": 1, "orange": 1},
            "banana": {"apple": 1, "orange": 1},
            "orange": {"banana": 1}
        }

    def test_valid_equivalence_class_1(self):
        """Valid equivalence class 1: both words exist and there are bridge words"""
        expected_output = "The bridge words from apple to banana are: orange"
        result = capture_output(self.graph.query_bridge_words, "apple", "banana")
        self.assertEqual(result.strip(), expected_output)

    def test_valid_equivalence_class_2(self):
        """Valid equivalence class 2: both words exist but there are no bridge words"""
        expected_output = "No bridge words from banana to apple!"
        result = capture_output(self.graph.query_bridge_words, "banana", "apple")
        self.assertEqual(result.strip(), expected_output)

    def test_invalid_equivalence_class_3(self):
        """Invalid equivalence class 3: at least one word does not exist"""
        expected_output = "No apple or xyz in the graph!"
        result = capture_output(self.graph.query_bridge_words, "apple", "xyz")
        self.assertEqual(result.strip(), expected_output)

    def test_invalid_equivalence_class_4(self):
        """Invalid equivalence class 4: both words are the same"""
        expected_output = "No bridge words from apple to apple!"
        result = capture_output(self.graph.query_bridge_words, "apple", "apple")
        self.assertEqual(result.strip(), expected_output)

def capture_output(func, *args, **kwargs):
    """捕获函数的输出"""
    # 保存标准输出
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # 执行函数
    func(*args, **kwargs)

    # 获取输出并恢复标准输出
    output = sys.stdout.getvalue()
    sys.stdout = original_stdout

    return output

if __name__ == '__main__':
    unittest.main()
