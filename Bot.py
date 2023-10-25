# Authors: Jasmean Fernando, Aileen Wu
# Description: This class initializes a Bot object.

import random
import math
from Cell import Cell

class Bot:
    # Constructor
    def __init__(self, cell):
        """
        Constructor that initializes a Bot object declared as self.
        
        :param: self, cell
        """
        self.cell = cell