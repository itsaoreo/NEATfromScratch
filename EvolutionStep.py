class EvolutionStep:

    def __init__(self, from_node_id, to_node_id, innov_num, innov_num_list):
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.innovation_num = innov_num
        self.innovation_num_list = innov_num_list.copy()

    # check if a step in evolution (ie an evolved structure) has already evolved before
    def equals(self, genome, from_node, to_node):
        # identical structures must have the same number of innovations ie number of added nodes and connections
        if len(genome.genes) == len(self.innovation_num_list):
            # todo: do we actually need to check to and from?
            if from_node.id == self.from_node_id and to_node.id == self.to_node_id:
                # check if innovation numbers are the same
                for i in range(len(genome.genes)):
                    if genome.genes[i].innovation_num not in self.innovation_num_list:
                        return False
                return True
        return False





