import random
from Node import Node
import Template
from ConnectionHistory import ConnectionHistory
from Connection import Connection


class Genome:
    def __init__(self, inputs_num, outputs_num):
        self.inputs_num = inputs_num
        self.outputs_num = outputs_num
        self.layers_num = 2
        self.next_node_num = 0
        self.bias_node = 0  # initialize at 0
        self.nodes = []  # list of nodes
        self.genes = []  # list of connections
        self.network_ordered = []  # list of nodes, ordered by when the neural network processes through them

        for i in range(inputs_num):
            new_input = Node(self.next_node_num)
            new_input.layer = 0
            self.next_node_num += 1
            self.nodes.append(new_input)

        for i in range(outputs_num):
            new_output = Node(self.next_node_num)
            new_output.layer = 1
            self.next_node_num += 1
            self.nodes.append(new_output)

        bias = Node(self.next_node_num)
        self.next_node_num += 1
        bias.layer = 0
        self.nodes.append(bias)

    def connect_nodes(self):

        for i in range(len(self.nodes)):
            self.nodes[i].output_links.clear()

        for i in range(len(self.genes)):
            self.genes[i].node_from.outputLink.add(self.genes[i])

    def add_connection(self, innovation_history_list):
        if self.connections_full():
            print("Network full. Add connection failed.")
            return

        from_index = int(random.uniform(0, len(self.nodes)))
        to_index = int(random.uniform(0, len(self.nodes)))

        while from_index == to_index or self.cannot_connect(from_index, to_index):
            from_index = int(random.uniform(0, len(self.nodes)))
            to_index = int(random.uniform(0, len(self.nodes)))

        from_node = self.genes[from_index]
        to_node = self.genes[to_index]

        connection_innov_num = self.get_innov_num(innovation_history_list, from_node, to_node)
        self.genes.append(Connection(from_node, to_node, random.uniform(-1, 1), connection_innov_num))  # may error
        self.connect_nodes()

    def connections_full(self):
        max = 0
        node_count_per_layer = []
        for i in range(len(self.nodes)):
            node_count_per_layer[self.nodes[i].layer] += 1

        for i in range(self.layers_num - 1):
            nodes_in_next = 0
            for j in range(i + 1, self.layers_num):
                nodes_in_next += node_count_per_layer[j]

            max += nodes_in_next * node_count_per_layer[i]

        return max == len(self.genes)

    def cannot_connect(self, to_index, from_index):
        if self.nodes[to_index].layer <= self.nodes[from_index].layer: return True  # if same layer or to is behind from
        # Finish for if the nodes are already connected! Dependency: isConnectedTo in Node class
        return False

    # innovation_history_list is a list of ConnectionHistories
    def get_innov_num(self, innovation_history_list, from_node, to_node):
        is_new = True
        connection_innov_num = Template.next_connection_num

        for i in range(len(innovation_history_list)):
            if innovation_history_list[i].equals(self, from_node, to_node):
                is_new = False
                connection_innov_num = innovation_history_list[i].innov_num
                break

        if is_new:
            self.update_innovation_history_list(innovation_history_list, from_node, to_node, connection_innov_num)
            Template.next_connection_num += 1

        return connection_innov_num

    def update_innovation_history_list(self, innovation_history_list, from_node, to_node, connection_innov_num):
        current_innov_nums = []
        for i in range(len(self.genes)):
            current_innov_nums.append(self.genes[i].innovation_num)

        innovation_history_list.append(
            ConnectionHistory(from_node.id, to_node.id, connection_innov_num, current_innov_nums))
