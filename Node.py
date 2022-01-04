class Node:
    def __init__(self, nodeKey):
        self.id = nodeKey
        self.inputLinks = []
        self.outputLink = []
        self.preActivationSum = 0
        self.outputValue = 0
        self.layer = 0

