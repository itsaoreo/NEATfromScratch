from _typeshed import Self
import numpy as np

class Node:
    def __init__(self, node_key):
        self.id = node_key
        self.output_connections = []
        self.pre_activation_sum = 0
        self.output_value = 0
        self.layer = 0

    def sigmoid(x):
        return (1.0 / (1.0 + np.exp(-x)))

    def engage():
        if Self.layer == 0:
            output_value = Node.sigmoid(Node.pre_actication_sum)
        

    def copy(self):
        copyNode = self.__init__(self, self.id)
        return copyNode

    def isConnected(other):
        #cant be connected if same layer
        if Self.layer == other.layer:
            return False

        if Self.layer > other.layer:    
            for i in range (len(other.output_connections)):
                if other.output_connections[i].to_node_id == Self:
                    return True
        elif  other.Selflayer > Self.layer:
            for i in range (len(Self.output_connections)):
                if Self.output_conections[i].to_node_id == other:
                    return True
        
        return False


        
        
