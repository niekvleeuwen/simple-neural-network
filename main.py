'''
    Tinlab ML Opdracht 2
    Authors
        - Niek van Leeuwen  0967267
        - Jordy van Essen   0968981
        - Tim de Jong       0968586
    
    Prioritized requirements:
        1. Differentiate crosses and circles trough machine learning
        2. Also differentiate between incomplete crosses and circles
        3. The usage of machine learning libraries is not allowed.

    Main design choices:
        1. We have created three main classes: Node, Edge en Neural Network
        2. The training and test data are read from a JSON file
        3. We save the trained network as a JSON file so we can minimize training
        4. We added a progressbar to track the training progress

    Test specification:
        1. During the predict cyclus we compare the expected results with the results
           provided by the network to caculate the accuracy of the network
        2. Some test data is only present in the testset
'''

from neuralNetwork import NeuralNetwork
from pathlib import Path

if __name__ == "__main__":
    # we have a 3x3 figure as input and two outcomes
    layers = (9, 10, 2)

    inputSetPath = Path.cwd() / 'dataset.json'
    n = NeuralNetwork(layers, inputSetPath)
    n.trainNetwork()
    n.predict()