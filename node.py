'''
    Authors
        - Niek van Leeuwen  
        - Jordy van Essen   
        - Tim de Jong       
'''
import numpy as np

class Node:
    """self, id"""
    def __init__(self, id):
        self.id = id
        self.incommingEdges = []
        self.outgoingEdges = []

    def getOutgoingEdges(self):
        return self.outgoingEdges

    def sigmoid(self, x):
        return 1 / (1 + np.exp((-x)))

    def addOutgoingEdge(self, edge):
        self.outgoingEdges.append(edge)
    
    def addIncommingEdge(self, edge):
        self.incommingEdges.append(edge)

    def caclulateEdges(self):
        total = 0
        for edge in self.incommingEdges:
            total += edge.getValue()
        return total

    def calculateValue(self):
        self.value = self.sigmoid(self.caclulateEdges())
        return self.value

    def getValue(self):
        return self.value
    
    def setValue(self, v):
        self.value = v
