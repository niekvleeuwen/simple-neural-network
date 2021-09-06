'''
    Author
        - Jordy van Essen       
'''
import sys

class Progressbar:
    def __init__(self, barLength):
        self.barLength = barLength
    
    def mapValue(self, currentRange, desiredRange, value):
        (currentMin, currentMax), (desiredMin, desiredMax) = currentRange, desiredRange
        return desiredMin + ((value - currentMin) * (desiredMax - desiredMin) / (currentMax - currentMin))
    
    def update(self, progress, duration):
        block = int(round(self.barLength * progress))
        text = f"\r[{'#' * block + '-' * (self.barLength - block)}] {(progress * 100.0):.1f}% {duration:.1f} s"
        sys.stdout.write(text)
        sys.stdout.flush()