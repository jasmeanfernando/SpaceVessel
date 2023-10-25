# Authors: Jasmean Fernando, Aileen Wu
# Description: This class initializes a Fire object.

import random
import math
from Cell import Cell

class Fire:
    # Constructor
    def __init__(self, cell):
        """
        Constructor that initializes a Fire object declared as self.
        
        :param: self, cell
        """
        self.cell = cell
        self.cell.on_fire = True