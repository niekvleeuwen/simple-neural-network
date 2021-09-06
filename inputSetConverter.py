'''
    Author
        - Jordy van Essen       
'''
import json as js

class InputSetConverter:
    def __init__(self):
        self.inputSet = dict()

    def createInputSet(self, filename):
        with open(filename) as inputSet:
            self.inputSet = js.load(inputSet)
        
        return self.inputSet