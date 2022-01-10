import random

from numpy import bitwise_and
from Node import Node
from EvolutionStep import EvolutionStep
from Connection import Connection

class Genome:
    next_connection_num = 0  # initialize connection numbers at 0

    def __init__(self, inputs_num, outputs_num):
        self.inputs_num = inputs_num
        self.outputs_num = outputs_num
        self.layers_num = 2
        self.next_node_num = 0
        self.bias_val = 0  # initialize bias at 0
        # self.bias_node = Node(-1) # -1 because uninitialized
        self.nodes = []  # list of nodes
        self.genes = []  # list of connections
        self.network_ordered = []  # list of nodes, ordered by layer for how the NN feeds forward through them
        # self.evolution_history = []  # list of EvolutionStep objects that shows how the unique genome structure
        # has evolved over time

        # initialize input nodes
        for i in range(inputs_num):
            new_input = Node(self.next_node_num)
            new_input.layer = 0
            self.next_node_num += 1
            self.nodes.append(new_input)

        # initialize output nodes
        for i in range(outputs_num):
            new_output = Node(self.next_node_num)
            new_output.layer = 1
            self.next_node_num += 1
            self.nodes.append(new_output)

        # initialize bias node
        self.bias_node = Node(self.next_node_num)
        self.next_node_num += 1
        self.bias_node.layer = 0
        self.nodes.append(self.bias_node)

    # mutation method 1. Add node to the nueral net
    def add_node(self, evolution_history):
        # if no connections exist, create one
        if len(self.genes) == 0:
            self.add_connection(evolution_history)
            return
        # 
        randomConnectionIndex = int(random.uniform(0, len(self.genes)))

        # cant remove bias node - check and re randomize if case
        while (self.genes[randomConnectionIndex].from_node.id == self.bias_node.id):
            randomConnectionIndex = int(random.uniform(0, len(self.genes)))

        self.genes[randomConnectionIndex].enabled = False

        newNodeNumber = self.next_node_num
        self.nodes.append(Node(newNodeNumber))
        self.next_node_num += 1

        # for connection bw a to b 
        connectionInnovationNumber = self.get_innov_num(evolution_history,
                                                        self.genes[randomConnectionIndex].from_node,
                                                        self.get_node(newNodeNumber))
        self.genes.append(Connection(self.genes[randomConnectionIndex].from_node, self.get_node(newNodeNumber), 1,
                                     connectionInnovationNumber))

        # for connection bw b to c
        connectionInnovationNumber = self.get_innov_num(evolution_history,
                                                        self.get_node(newNodeNumber),
                                                        self.genes[randomConnectionIndex].to_node)
        self.genes.append(Connection(self.get_node(newNodeNumber),
                                     self.genes[randomConnectionIndex].to_node,
                                     self.genes[randomConnectionIndex].weight,
                                     connectionInnovationNumber))
        self.get_node(newNodeNumber).layer = self.genes[randomConnectionIndex].from_node.layer + 1

        # get innovation number for bias connection
        connectionInnovationNumber = self.get_innov_num(evolution_history,
                                                        self.get_node(self.bias_node),
                                                        self.get_node(newNodeNumber))
        # insert connection to bias node 
        self.genes.append(Connection(self.get_node(self.bias_node), self.get_node(newNodeNumber),
                                     0, connectionInnovationNumber))

        if self.get_node(newNodeNumber).layer == self.genes[randomConnectionIndex].to_node.layer:
            for i in range(len(self.nodes) - 1):
                if self.nodes[i].layer >= self.get_node(newNodeNumber):
                    self.nodes[i].layer += 1
            self.layers += 1

        self.connect_nodes()
        return

    # todo: Arya pls see this
    # todo: fix all the instance methods where self is not the first param and update function body accordingly
    # todo: eg. Self.nodes -> self.nodes I deleted the import _typeShed Self so the errors aren't hidden
    # todo: also u need to use range(len(...)) bc range converts int to iterable
    # return the node pos with the matching ID or returns none
    def get_node(self, searchID):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == searchID:
                return self.nodes[i]
        return None

    # Connects nodes by loading up each node's output_connections list
    def connect_nodes(self):

        # clear the output connections of each node
        for i in range(len(self.nodes)):
            self.nodes[i].output_connections.clear()

        # for each connection, get that connection's from_node and add the connection to that
        # node's output connections list
        for i in range(len(self.genes)):
            self.genes[i].node_from.output_connections.append(self.genes[i])

    # Mutation method #2: Generate a random connection
    def add_connection(self, innovation_history_list):
        # Check if the neural net is full ie no new connections can be added
        if self.is_full():
            print("Network full. Add connection failed.")
            return

        # Generate 2 random indices
        from_index = int(random.uniform(0, len(self.nodes)))
        to_index = int(random.uniform(0, len(self.nodes)))

        # Keep generating until you get a legal connection between 2 nodes
        while from_index == to_index or self.cannot_connect(from_index, to_index):
            from_index = int(random.uniform(0, len(self.nodes)))
            to_index = int(random.uniform(0, len(self.nodes)))

        # Get those random nodes
        from_node = self.genes[from_index]
        to_node = self.genes[to_index]

        # Get the innovation number for this mutation
        connection_innov_num = self.get_innov_num(from_node, to_node)
        # Add this connection with a random weight and the innovation number to the list of connections
        self.genes.append(Connection(from_node, to_node, random.uniform(-1, 1), connection_innov_num))
        # Connect nodes
        self.connect_nodes()

    # Checks if the neural network is full
    def is_full(self):
        max_possible = 0
        # List to keep track of how many nodes are in each layer
        node_count_per_layer = []
        for i in range(len(self.nodes)):
            node_count_per_layer[self.nodes[i].layer] += 1

        # Maximum connections per layer is given by the number of nodes in that layer * the number of nodes ahead of it
        # For each layer,
        for i in range(self.layers_num - 1):
            nodes_ahead = 0
            # Go through the layers ahead of it
            for j in range(i + 1, self.layers_num):
                # Add the number of nodes in each layer ahead of it
                nodes_ahead += node_count_per_layer[j]
            # Multiple by the number of nodes in this layer, and add it to the total
            max_possible += nodes_ahead * node_count_per_layer[i]

        return max_possible == len(self.genes)

    # Checks if two nodes can connect
    def cannot_connect(self, from_index, to_index):
        # if the indices are the same, thus pointing to the same node
        # this check is also in the relevant while loop in add_connection() for optimization
        if from_index == to_index:
            return True
        # if same layer or from is in front of to
        if self.nodes[from_index].layer >= self.nodes[to_index].layer:
            return True
        # if the two nodes are already connected
        if self.nodes[from_index].is_connected(self.nodes[to_index]):
            return True
        return False

    # Gets an innovation number for the resultant genome of a mutation
    def get_innov_num(self, evolution_history, from_node, to_node):
        is_new = True
        connection_innovation_num = Genome.next_connection_num

        # If the genome has been generated before, then use the innovation number of that earlier evolution
        for i in range(len(evolution_history)):
            if evolution_history[i].equals(self, from_node, to_node):
                is_new = False
                connection_innovation_num = evolution_history[i].innovation_num
                break

        # If it's a new genome, record this new evolution and give it the next innovation number.
        if is_new:
            self.record_new_evolution(evolution_history, from_node.id, to_node.id, connection_innovation_num)
            Genome.next_connection_num += 1

        return connection_innovation_num

    # Records a new evolution as an EvolutionStep object added to a passed in list of all evolved genomes
    def record_new_evolution(self, evolution_history, from_node_id, to_node_id, connection_innov_num):
        innovation_num_list = []
        # Record all the existing EvolutionSteps up to this point, not counting
        for i in range(len(self.genes)):
            innovation_num_list.append(self.genes[i].innovation_num)
        new_evolution = EvolutionStep(from_node_id, to_node_id, connection_innov_num, innovation_num_list)
        evolution_history.append(new_evolution)
