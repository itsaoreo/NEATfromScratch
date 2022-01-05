class Node:
    def __init__(self, node_key):
        self.id = node_key
        self.input_links = []
        self.output_links = []
        self.pre_activation_Sum = 0
        self.output_value = 0
        self.layer = 0

