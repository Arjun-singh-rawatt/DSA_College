import tempfile
import unittest
from pathlib import Path

from algorithms.dp_algorithms import knapsack_01, lcs_length, matrix_chain_order, resource_allocation
from algorithms.graph_algorithms import bellman_ford, bfs, dfs, dijkstra, kruskal, prim
from data_loader import DataLoadError, Student, load_students
from student_structures import CGPATree, build_lookup, find_student, top_students


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.students = [
            Student("ST-002", "B", 8.5, 90, 80, 70),
            Student("ST-001", "A", 8.5, 80, 90, 70),
            Student("ST-003", "C", 7.0, 90, 80, 70),
        ]

    def test_lookup_is_case_insensitive_and_numeric_roll_resolves(self):
        index = build_lookup(self.students)
        self.assertEqual(find_student(index, " st-001 ").name, "A")
        self.assertEqual(find_student(index, "1").erp, "ST-001")
        self.assertIsNone(find_student(index, "ST-999"))

    def test_bst_keeps_duplicate_cgpa_and_inclusive_bounds(self):
        tree = CGPATree(self.students)
        self.assertEqual([s.erp for s in tree.in_range(8.5, 8.5)], ["ST-001", "ST-002"])
        self.assertEqual(len(tree.in_range()), 3)

    def test_heap_ranking_tie_uses_erp_ascending(self):
        self.assertEqual([s.erp for s in top_students(self.students, 3, "CGPA")], ["ST-001", "ST-002", "ST-003"])
        self.assertEqual([s.erp for s in top_students(self.students, 2, "Operating Systems")], ["ST-002", "ST-003"])

    def test_loader_reports_bad_duplicate_and_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "students.txt"
            path.write_text("ERP|Name|CGPA|OperatingSystems|DSA|Mathematics\nST-1|One|9|80|70|60\n", encoding="utf-8")
            self.assertEqual(len(load_students(path)), 1)
            path.write_text("ST-1|One|9|80|70|60\nst-1|Two|8|70|60|50\n", encoding="utf-8")
            with self.assertRaisesRegex(DataLoadError, "duplicate"):
                load_students(path)
            path.write_text("ST-1|One|11|80|70|60\n", encoding="utf-8")
            with self.assertRaisesRegex(DataLoadError, "between 0 and 10"):
                load_students(path)

    def test_graph_traversal_paths_and_mst(self):
        graph = {"A": [("B", 1), ("C", 4)], "B": [("A", 1), ("C", 2)], "C": [("A", 4), ("B", 2)]}
        self.assertEqual(bfs({"A": ["B", "C"], "B": ["A"], "C": ["A"]}, "A"), ["A", "B", "C"])
        self.assertEqual(set(dfs({"A": ["B", "C"], "B": ["A"], "C": ["A"]}, "A")), {"A", "B", "C"})
        self.assertEqual(prim(graph)[1], 3)
        self.assertEqual(kruskal(graph)[1], 3)
        self.assertEqual(dijkstra(graph, "A")["C"], 3)
        self.assertEqual(bellman_ford({"A": [("B", 2)], "B": [("C", -1)], "C": []}, "A")["C"], 1)
        with self.assertRaisesRegex(ValueError, "negative-weight cycle"):
            bellman_ford({"A": [("B", 1)], "B": [("A", -2)]}, "A")
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            dijkstra({"A": [("B", -1)], "B": []}, "A")

    def test_dp_examples(self):
        self.assertEqual(knapsack_01([1, 3, 4], [15, 20, 30], 4), 35)
        self.assertEqual(lcs_length("ABCBDAB", "BDCABA"), 4)
        self.assertEqual(matrix_chain_order([10, 30, 5, 60]), 4500)
        self.assertEqual(resource_allocation([[0, 1, 4], [0, 2, 3]], 2), 4)


if __name__ == "__main__":
    unittest.main()
