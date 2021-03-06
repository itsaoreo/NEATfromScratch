import unittest

from Connection import Connection
from Node import Node


class MyTestCase(unittest.TestCase):
    def test_mutate_weight(self):
        weights = []
        for i in range(1000):
            node_test_from = Node(1)
            node_test_to = Node(0)
            con_test = Connection(node_test_from, node_test_to, 0, 10)
            con_test.mutate_weight()
            weights.append(con_test.weight)
        self.assertFalse(0 in weights, "Original weight not changed")
        self.assertAlmostEqual(sum(weights)/1000, 0, None, "Weights not centered at 0", .2)

    def test_copy_connection(self):
        node_test_from = Node(1)
        node_test_to = Node(0)
        con_test = Connection(node_test_from, node_test_to, 0, 10)
        con_copy = con_test.copy()
        self.assertNotEqual(con_copy, con_test)
        self.assertEqual(con_copy.weight, con_test.weight)
        self.assertEqual(con_copy.to_node, con_test.to_node)
        self.assertNotEqual(con_copy.from_node, con_test.to_node)
        self.assertEqual(con_copy.to_node.id, con_test.to_node.id)
        self.assertEqual(con_copy.from_node.id, con_test.from_node.id)


if __name__ == '__main__':
    unittest.main()
