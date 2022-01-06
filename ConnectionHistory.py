class ConnectionHistory:

    def __init__(self, from_node_id, to_node_id, innov_num, innov_num_list):
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.innovation_num = innov_num
        self.innovation_num_list = innov_num_list.copy()

    def equals(self, genome, from_node, to_node):
        if len(genome.genes) == len(self.innov_num_list):
            if from_node.id == self.from_node_id and to_node.id == self.to_node_id:
                for i in range(len(genome.genes)):
                    if genome.genes[i].innovation_num in self.innov_num_list:
                        return False
                return True
        return False





