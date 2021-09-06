'''
    Authors
        - Niek van Leeuwen  
        - Jordy van Essen   
        - Tim de Jong       
'''

import numpy as np
import time as tm
import json as js
import os
import click

from edge import Edge
from node import Node
from progressbar import Progressbar
from inputSetConverter import InputSetConverter

class NeuralNetwork:
    '''
        layerSizes is a tuple with the amount of nodes for all the layers
    '''
    def __init__(self, layers, inputSetPath):
        self.setConverter = InputSetConverter()
        inputSet = self.setConverter.createInputSet(inputSetPath)
        self.trainingsSet = inputSet['trainingsSet']
        self.testSet = inputSet['testSet']
        self.figures = inputSet['figures']

        self.networkData = self.setConverter.createInputSet("neuralnetworkEdgeValues.json")
        self.networkTrained = self.networkData['networkTrained']
        self.accuracy = self.networkData['networkAccuracy']

        if self.networkTrained:
            if click.confirm("This network is already trained. Would you like to train again?", default=True):
                self.networkTrained = False

        self.layers = self.createLayers(len(layers), layers)
        self.inputLayer = self.layers[0]
        self.outputLayer = self.layers[len(self.layers) - 1]

        self.linkAllNodes()

    def createLayers(self, amount, size):
        layers = []
        for i in range(amount):
            layers.append( [Node(nodeId) for nodeId in range(size[i])] )
        
        return tuple(layers)

    def assignInput(self, inputValues):
        for node, value in zip(self.inputLayer, inputValues):
            node.setValue(value)

    def linkAllNodes(self):
        edgeId = 0
        for i in range(len(self.layers) - 1):
            if i + 1 < len(self.layers):
                for nodeIn in self.layers[i]:
                    for nodeOut in self.layers[i + 1]:
                        edge = Edge(edgeId, 1, nodeIn, nodeOut)

                        if self.networkTrained:
                            edge.setAmplifier(self.networkData['edgeValues'][f'{edgeId}'])

                        nodeOut.addIncommingEdge(edge)
                        nodeIn.addOutgoingEdge(edge)
                        edgeId += 1
    
    def getAllEdges(self):
        allEdges = []
        for layer in self.layers:
            for node in layer:
                nodeOutgoingEdges = node.getOutgoingEdges()
                for edge in nodeOutgoingEdges:
                    allEdges.append(edge)
        return allEdges

    def saveNetwork(self):
        self.networkData['networkTrained'] = True
        self.networkData['networkAccuracy'] = self.accuracy

        self.networkData['edgeValues'] = dict()
        edges = self.getAllEdges()
        for edge in edges:
            self.networkData['edgeValues'][f'{edge.getId()}'] = edge.getAmplifier()

        with open('neuralNetworkEdgeValues.json', 'w') as file:
            file.write(js.dumps(self.networkData, indent = 4))

    def trainNetwork(self):
        bestEdge = None
        bestValue = None
        avgError = np.Infinity
        desiredAvgError = 0.00001

        progressBar = Progressbar(50)
        startTime = tm.time()
        firstLoop = True
        currentRange = tuple()
        desiredRange = (0, 1)

        allEdges = self.getAllEdges()
        
        if self.networkTrained:
            print(f"Network already trained. Accuracy: {self.accuracy} %")
            return

        print("Training neural network")
        while avgError > desiredAvgError:
            currentBestError = np.Infinity
            for edge in allEdges:
                for value in [-0.1, 0.1]:
                    # change the amplifier of one edge
                    edge.changeAmplifier(value)

                    newAvgError = self.calculateError(self.trainingsSet)
                    
                    # reset the amplifier to the original state
                    edge.changeAmplifier(-value)

                    if newAvgError < currentBestError:
                        # set range of the progressbar
                        if firstLoop:
                            firstLoop = False
                            currentRange = (newAvgError, desiredAvgError)

                        currentBestError = newAvgError
                        bestEdge = edge
                        bestValue = value

            if not self.networkTrained:
                progressBar.update(progressBar.mapValue(currentRange, desiredRange, newAvgError), tm.time() - startTime)

            # only change the amplifier that has the most positive effect on the error
            bestEdge.changeAmplifier(bestValue)
            avgError = currentBestError

        self.accuracy = round(100.0 - avgError, 6)
        print(f"\nFinished training neural network. Accuracy: {self.accuracy} %\n\n")    
        self.saveNetwork()

    def calculateError(self, set, log=False):
        totalError = 0
        # calculate the error for each entry in the training data
        for i in range(len(set)):
            # give the current figure in the training data to the the input edges
            self.assignInput(set[f'{i}']['input'])

            # calculate the new values
            for layer in self.layers:
                if layer is not self.inputLayer:
                    for node in layer:
                        node.calculateValue()
            
            # get the result from the output layer
            result = []
            for endNode in self.outputLayer:
                result.append(endNode.calculateValue())                      
            
            expectedResult = self.figures[set[f'{i}']['figure']]
            
            # normalise result vector
            result /= np.linalg.norm(result)
            currentError = np.mean((result - expectedResult) ** 2)

            if log:
                figure = set[f'{i}']['input']

                print("=============================\nFigure:")
                for index, item in enumerate(figure, start=1):
                    print(item, end=' ' if index % 3 else '\n')

                expectedFigure = set[f'{i}']['figure']
                print(f"\nExpected result: {expectedFigure}")
                print(f"Actual result: {'X' if result[0] > result[1] else 'O'} -> {((1.0 - currentError) * 100):.4f} % confidence.") 

            # caculate the mean square error
            totalError += currentError
        
        # calculate total average error with the updated value
        return totalError / len(set)

    def predict(self):
        print(f"\n\nThe calculated accuracy over the whole testset: {(1.0 - self.calculateError(self.testSet, True)) * 100.0:.4f} %")
          