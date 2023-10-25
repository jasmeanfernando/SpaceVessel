# Authors: Jasmean Fernando, Aileen Wu
# Description: This class initializes cells used to build the (D x D) square grid layout for the spaceship.

import decimal

# Set precision for decimal values.
decimal.getcontext().prec = 5

class Cell:
    # Constructor
    def __init__(self, x, y):
        """
        Constructor that initializes a Cell object declared as self.
        
        :param: self, x, y
        """
        self.x = x
        self.y = y
        self.is_open = False
        self.on_fire = False
        self.flammability = decimal.Decimal(0)

    # Equals Method
    def __eq__(self, other_cell):
        """
        Method that checks if two cells are equal.
        
        :param: self, other_cell
        :return: true if two cells are equal, false otherwise.
        """
        if self.x == other_cell.x and self.y == other_cell.y:
            return True
        else:
            return False
    
    # Comparision Method
    def __lt__(self, other_cell):
        """
        Method that compares two cells.
        
        :param: self, other_cell
        :return: true if two cells are equal, false otherwise.
        """
        if self.x < other_cell.x:
            return True
        elif self.x == other_cell.x:
            return self.y < other_cell.y
        else:
            return False
    
    # Change Flammability Method
    def change_flammability(self, q, k):
        """
        Method that changes flammability of cell based on flammability of ship (q) and number of neighboring cells on fire (k).
        
        :param: self, q, k
        """
        q = decimal.Decimal(q)

        if k == 0:
            self.flammability = decimal.Decimal(0)
        else:
            self.flammability = 1 - (1 - q) ** k
    
    # HashMap Method
    def __hash__(self):
        """
        Method that creates HashMap representation of cell.
        
        :param: self
        :return: hashmap of cell.
        """
        return hash((self.x, self.y))