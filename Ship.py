# Authors: Jasmean Fernando, Aileen Wu
# Description: This class initializes the (D x D) square grid layout for the spaceship based on particular specifications.

import decimal
import random
from Cell import Cell
from Bot import Bot
from Button import Button
from Fire import Fire

# Set precision for decimal values.
decimal.getcontext().prec = 5

class Ship:
    # Constructor
    def __init__(self, d, q):
        """
        Constructor that initializes a Ship object declared as self.
        
        :param: self, d, q
        """
        # Ship size
        self.d = d
        # Ship flammability
        self.q = q
        # (D x D) square grid layout: x -> rows, y -> columns
        self.grid = [[Cell(x, y) for y in range(d)] for x in range(d)]
        # List of blocked cells with 1 open neighbor
        self.blocked_cells_w_one_open_neighbor = []
        # List of open cells with 1 open neighbor (dead-ends)
        self.dead_ends = []
        # List of open cells near fire
        self.opened_cells_near_fire = []
        # List of cells on fire
        self.cells_on_fire = []

        self.bot = None
        self.button = None
        self.initial_fire = None

    # Print Method
    def __str__(self):
        """
        Default method that prints a Ship object declared as self.
        
        :param: self
        """
        s = "Ship:\n"
        for x in range(self.d):
            for y in range(self.d):
                if self.grid[x][y].on_fire is True:
                    s += "[🔥]"
                elif self.bot != None and self.grid[x][y] == self.bot.cell:
                    s += "[🤖]"
                elif self.button != None and self.grid[x][y] == self.button.cell:
                    s += "[🔘]"
                elif self.grid[x][y].is_open is True:
                    s += "[  ]"
                else:
                    s += "[🔒]"
            s += "\n"
        return s

    def spawn_bot(self):
        """
        Method that spawns a bot object in random open cell.
        
        :param: self
        """
        test_cell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        # Randomly chooses a cell to spawn in the bot; If that cell is closed, re-choose.
        while test_cell.is_open is False:
            test_cell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        self.bot = Bot(test_cell)

    def spawn_button(self):
        """
        Method that spawns a button object in random open cell.
        
        :param: self
        """
        test_cell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        # Randomly chooses a cell to spawn in the button; If that cell is closed, re-choose.
        while test_cell.is_open is False or test_cell == self.bot.cell:
            test_cell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        self.button = Button(test_cell)

    def spawn_initial_fire(self):
        """
        Method that spawns a fire object in random open cell.
        
        :param: self
        """
        test_cell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        # Randomly chooses a cell to spawn in the initial fire; If that cell is closed, re-choose.
        while test_cell.is_open is False or test_cell == self.button.cell or test_cell == self.bot.cell:
            test_cell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        self.initial_fire = Fire(test_cell)
        # Start inital fire.
        self.set_on_fire(test_cell.x, test_cell.y)
        self.cells_on_fire.append(self.grid[test_cell.x][test_cell.y])

    # Check Cell's Open Neighbors Method
    def has_single_open_neighbor(self, cell):
        """
        Method that checks whether a cell has only /one/ open neighbor.
        
        :param: self, cell
        :return: true if it has only one open neighbor, false otherwise.
        """
        num_neighbors = 0
        
        # Exit loop if more than two open neighbors found.
        while (num_neighbors < 2):
            # Check left:
            if cell.x - 1 >= 0:
                if self.grid[cell.x - 1][cell.y].is_open is True:
                    num_neighbors += 1
            # Check right:
            if cell.x + 1 < self.d:
                if self.grid[cell.x + 1][cell.y].is_open is True:
                    num_neighbors += 1
            # Check up:
            if cell.y + 1 < self.d:
                if self.grid[cell.x][cell.y + 1].is_open is True:
                    num_neighbors += 1
            # Check down:
            if cell.y - 1 >= 0:
                if self.grid[cell.x][cell.y - 1].is_open is True:
                    num_neighbors += 1
            
            if num_neighbors == 1:
                return True
            return False
    
    # Open Cell Method
    def open_cell(self, x, y):
        """
        Method that opens a cell (x, y), updates dead_ends list, and updates blocked_cells_w_one_open_neighbor list.
        
        :param: self, x, y
        """
        # Base Case: If cell is already open, do nothing.
        # Accounts for duplicates.
        if self.grid[x][y].is_open is True:
            return

        # Open cell.
        self.grid[x][y].is_open = True

        # Update dead_ends list.
        # If cell already has only /one/ open neighbor and is NOT in dead_ends -> append it to dead_ends.
        if self.has_single_open_neighbor(self.grid[x][y]) is True and self.grid[x][y] not in self.dead_ends:
            self.dead_ends.append(self.grid[x][y])
        
        # Else if, cell does not have only /one/ open neighbor and is in dead_ends -> remove it.
        # This is because dead-ends can revert back to a normal cell.
        elif self.has_single_open_neighbor(self.grid[x][y]) is False and self.grid[x][y] in self.dead_ends:
            self.dead_ends.remove(self.grid[x][y])

        # Update blocked_cells_w_one_open_neighbor list.
        # Check left:
        if x - 1 >= 0:
            # If left neighbor of cell is blocked cell with only one neighbor -> append it to blocked_cells_w_one_open_neighbor.
            if self.grid[x - 1][y].is_open is False and self.has_single_open_neighbor(self.grid[x - 1][y]) is True:
                self.blocked_cells_w_one_open_neighbor.append(self.grid[x - 1][y])
            
            # Else if, left neighbor of cell is in blocked_cells_w_one_open_neighbor -> remove it.
            # This is because cell was previously checked and already has an open neighbor. Now, cell has TWO open neighbors.
            elif self.grid[x - 1][y] in self.blocked_cells_w_one_open_neighbor:
                self.blocked_cells_w_one_open_neighbor.remove(self.grid[x - 1][y])
        # Check right:
        if x + 1 < self.d:
            if self.grid[x + 1][y].is_open is False and self.has_single_open_neighbor(self.grid[x + 1][y]) is True:
                self.blocked_cells_w_one_open_neighbor.append(self.grid[x + 1][y])
            
            elif self.grid[x + 1][y] in self.blocked_cells_w_one_open_neighbor:
                self.blocked_cells_w_one_open_neighbor.remove(self.grid[x + 1][y])
        # Check up:
        if y + 1 < self.d:
            if self.grid[x][y + 1].is_open is False and self.has_single_open_neighbor(self.grid[x][y + 1]) is True:
                self.blocked_cells_w_one_open_neighbor.append(self.grid[x][y + 1])
            
            elif self.grid[x][y + 1] in self.blocked_cells_w_one_open_neighbor:
                self.blocked_cells_w_one_open_neighbor.remove(self.grid[x][y + 1])      
        # Check down:
        if y - 1 >= 0:
            if self.grid[x][y - 1].is_open is False and self.has_single_open_neighbor(self.grid[x][y - 1]) is True:
                self.blocked_cells_w_one_open_neighbor.append(self.grid[x][y - 1])
            
            elif self.grid[x][y - 1] in self.blocked_cells_w_one_open_neighbor:
                self.blocked_cells_w_one_open_neighbor.remove(self.grid[x][y - 1])

    # Open Dead-End Cell Method
    def open_dead_end(self, cell):
        """
        Method that opens a dead-end cell by opening /one/ of its blocked neighbor.
        
        :param: self, cell
        """
        # Base Case: If cell is not a dead-end cell (open cell with one open neighbor), do nothing.
        if cell.is_open is False or self.has_single_open_neighbor(cell) is False:
            return

        # Randomly loop through the dead-end cell's neighbors until it finds one that is blocked.
        while True:
            i = random.randint(1, 4)
            # Open left:
            if i == 1 and cell.x - 1 >= 0 and self.grid[cell.x - 1][cell.y].is_open is False:
                self.grid[cell.x - 1][cell.y].is_open = True
                self.dead_ends.remove(cell)
                return
            # Open right:
            if i == 2 and cell.x + 1 < self.d and self.grid[cell.x + 1][cell.y].is_open is False:
                self.grid[cell.x + 1][cell.y].is_open = True
                self.dead_ends.remove(cell)
                return
            # Open up:
            if i == 3 and cell.y + 1 < self.d and self.grid[cell.x][cell.y + 1].is_open is False:
                self.grid[cell.x][cell.y + 1].is_open = True
                self.dead_ends.remove(cell)
                return
            # Open down:
            if i == 4 and cell.y - 1 >= 0 and self.grid[cell.x][cell.y - 1].is_open is False:
                self.grid[cell.x][cell.y - 1].is_open = True
                self.dead_ends.remove(cell)
                return
    
    # Check Cell's Open Neighbors On Fire Method
    def has_open_neighbors_on_fire(self, cell):
        """
        Method that checks whether a cell has open neighbors on fire.
        
        :param: self, cell
        :return: number of open neighbors on fire.
        """
        num_neighbors = 0

        # Check left:
        if cell.x - 1 >= 0:
            if self.grid[cell.x - 1][cell.y].is_open is True and self.grid[cell.x - 1][cell.y].on_fire is True:
                num_neighbors += 1
        # Check right:
        if cell.x + 1 < self.d:
            if self.grid[cell.x + 1][cell.y].is_open is True and self.grid[cell.x + 1][cell.y].on_fire is True:
                num_neighbors += 1
        # Check up:
        if cell.y + 1 < self.d:
            if self.grid[cell.x][cell.y + 1].is_open is True and self.grid[cell.x][cell.y + 1].on_fire is True:
                num_neighbors += 1
        # Check down:
        if cell.y - 1 >= 0:
            if self.grid[cell.x][cell.y - 1].is_open is True and self.grid[cell.x][cell.y - 1].on_fire is True:
                num_neighbors += 1
        
        return num_neighbors
    
    # Set On Fire Method
    def set_on_fire(self, x, y):
        """
        Method that sets an open cell on fire.
        
        :param: self, x, y
        """
        # Set cell on fire.
        self.grid[x][y].on_fire = True
        
        # Update opened_cells_near_fire list:
        # No need to spread fire to a cell that is already on fire.
        if self.grid[x][y] in self.opened_cells_near_fire:
            self.opened_cells_near_fire.remove(self.grid[x][y])
        
        # Spread fire to open cells that are not already on fire.
        # Check left:
        if x - 1 >= 0 and self.grid[x - 1][y].is_open is True and self.grid[x - 1][y].on_fire is False:
            # Update flammability of neighboring cells.
            k = self.has_open_neighbors_on_fire(self.grid[x - 1][y])
            self.grid[x - 1][y].change_flammability(self.q, k)
            # Append to opened_cells_near_fire list.
            self.opened_cells_near_fire.append(self.grid[x - 1][y])
        # Check right:
        if x + 1 < self.d and self.grid[x + 1][y].is_open is True and self.grid[x + 1][y].on_fire is False:
            k = self.has_open_neighbors_on_fire(self.grid[x + 1][y])
            self.grid[x + 1][y].change_flammability(self.q, k)
            self.opened_cells_near_fire.append(self.grid[x + 1][y])
        # Check up:
        if y + 1 < self.d and self.grid[x][y + 1].is_open is True and self.grid[x][y + 1].on_fire is False:
            k = self.has_open_neighbors_on_fire(self.grid[x][y + 1])
            self.grid[x][y + 1].change_flammability(self.q, k)
            self.opened_cells_near_fire.append(self.grid[x][y + 1])
        # Check down:
        if y - 1 >= 0 and self.grid[x][y - 1].is_open is True and self.grid[x][y - 1].on_fire is False:
            k = self.has_open_neighbors_on_fire(self.grid[x][y - 1])
            self.grid[x][y - 1].change_flammability(self.q, k)
            self.opened_cells_near_fire.append(self.grid[x][y - 1])
    
    # Advance Fire Method
    def advance_fire(self):
        """
        Method that advances fire based on the probability of cells near fire catching on fire.
        
        :param: self
        """
        # Initialize random threshold between 0 and 1.
        threshold = random.random()
        
        # For all current cells near fire:
        for cell in self.opened_cells_near_fire[:]: # Iterate through a local copy of self.opened_cells_near_fire.
            # Set cell on fire if above threshold.
            if (cell.flammability >= threshold):
                self.set_on_fire(cell.x, cell.y)
                self.cells_on_fire.append(self.grid[cell.x][cell.y])