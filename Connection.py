import random


class Connection:
    def __init__(self, node_from, node_to, weight, innovation_num):
        self.node_from = node_from
        self.node_to = node_to
        self.weight = weight
        self.innovation_num = innovation_num
        self.enabled = True

    def mutate_weight(self):
        prob = random.uniform(0, 1)
        if prob < .1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1) / 10
            if self.weight > 1:
                self.weight = 1
            elif self.weight < -1:
                self.weight = -1

    def clone(self):
        clone_connection = self.__init__(self.node_from, self.node_to, self.weight, self.innovation_num)
        clone_connection.enabled = self.enabled
        return clone_connection
