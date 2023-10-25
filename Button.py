# Authors: Jasmean Fernando, Aileen Wu
# Description: This class initializes a Button object.

import random
import math
from Cell import Cell

class Button:
    # Constructor
    def __init__(self, cell):
        """
        Constructor that initializes a Button object declared as self.
        
        :param: self, cell
        """
        self.cell = cell