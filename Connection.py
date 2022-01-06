import random


class Connection:
    def __init__(self, from_node, to_node, weight, innovation_num):
        self.to_node = to_node
        self.from_node = from_node
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
        clone_connection = self.__init__(self.from_node, self.to_node, self.weight, self.innovation_num)
        clone_connection.enabled = self.enabled
        return clone_connection
