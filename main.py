# Authors: Jasmean Fernando, Aileen Wu
# Description: This class is used to run the SpaceVessel.

import decimal
import random
import math
from Ship import Ship

def main():
    # Get user input for spaceship specifications (size and flammability).
    print('Enter an integer D to define a (D x D) square grid layout of the Archaeopteryx space vessel:')
    d = int(input())
    print('Enter a decimal q between 0 and 1 to define the flammability of the Archaeopteryx space vessel:')
    q = decimal.Decimal(input())

    # Initialize the spaceship.
    ship = Ship(d, q)

    # Generate cell position at random.
    x = random.randint(0, d - 1)
    y = random.randint(0, d - 1)

    # Open cell position on spaceship.
    ship.open_cell(x, y)
    print(ship)

if __name__ == "__main__":
    main()