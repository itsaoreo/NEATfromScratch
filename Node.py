#from _typeshed import Self
import numpy as np


class Node:
    def __init__(self, node_key):
        self.id = node_key
        self.output_connections = []
        self.pre_activation_sum = 0
        self.output_value = 0
        self.layer = 0

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-1 * x))

    def engage(self):
        if self.layer == 0:
            output_value = self.sigmoid(self.pre_activation_sum)
        for i in range(len(self.output_connections)):
            if self.output_connections[i].enabled:
                self.output_connections[i].to_node.pre_activation_sum += self.output_connections[
                                                                             i].weight * self.output_value

    def copy(self):
        copy_node = Node.__init__(self, self.id)
        return copy_node

    def is_connected(self, other):
        # cant be connected if same layer
        if self.layer == other.layer:
            return False

        if self.layer > other.layer:
            for i in range(len(other.output_connections)):
                if other.output_connections[i].to_node == self: # reference equality on objects?
                    return True
        elif other.layer > self.layer:
            for i in range(len(self.output_connections)):
                if self.output_connections[i].to_node == other:
                    return True

        return False
