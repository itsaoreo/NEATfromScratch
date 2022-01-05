import random
from Node import Node


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

        # connection_innov_num = not complete



    def connections_full(self):
        max = 0
        node_count_per_layer = []
        for i in range(len(self.nodes)):
            node_count_per_layer[self.nodes[i].layer] += 1

        for i in range(self.layers_num - 1):
            nodes_in_next = 0
            for j in range (i + 1, self.layers_num):
                nodes_in_next += node_count_per_layer[j]

            max += nodes_in_next * node_count_per_layer[i]

        return max == len(self.genes)

    def cannot_connect(self, to_index, from_index):
        if self.nodes[to_index].layer <= self.nodes[from_index].layer: return True # if same layer or to is behind from
        # Finish for if the nodes are already connected! Dependency: isConnectedTo in Node class
        return False

    def getInnovNum(self, innovation_history_list, from_node, to_node):
        is_new = True
        connection_innov_num = 0 # check the template bc this is some bullshit -- what is nextConnectionNo?
        next_connection_num = 0
        
        #for i in range(len(innovation_history_list)):
            # if (innovation_history_list[i].) # must implement matches dependencies in connectionHistory
