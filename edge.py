'''
    Authors
        - Niek van Leeuwen  
        - Jordy van Essen   
        - Tim de Jong       
'''
class Edge:

    """self, id, value, originNode, destinationNode"""
    def __init__(self, id, value, originNode, destinationNode):
        self.id = id
        self.originNode = originNode
        self.destinationNode = destinationNode
        
        self.setAmplifier(1)

    def getId(self):
        return self.id
    
    def getAmplifier(self):
        return self.amplifier

    def setAmplifier(self, amplifier):
        self.amplifier = amplifier

    def setValue(self, value):
        self.destinationNode.setValue(value)

    def changeAmplifier(self, magnitude):
        self.amplifier += magnitude

    def getValue(self):
        return self.originNode.getValue() * self.amplifier
