# Authors: Jasmean Fernando, Aileen Wu
# Description: This class is used to run the SpaceVessel.

import copy
import decimal
import random
import math
import queue
from queue import Queue
from collections import deque
from Ship import Ship
from Bot import Bot

# Set precision for decimal values.
decimal.getcontext().prec = 5

# Dictionary used to keep track of cell's danger factor (probability of catching on fire) -> used by Bot4.
ship_danger_factors = {}

# Bot1 Method
def run_bot1(ship):
    """
    Method used to run Bot1 via Breadth-First Search.

    :return: true if bot was able to reach button, or false otherwise.
    """
    fringe = Queue() # For BFS.
    closed_set = set() # Tracks visited cells.
    prev = {ship.bot.cell : ship.bot.cell} # Tracks parent.

    fringe.put(ship.bot.cell)
    
    while fringe.empty() is False:
        curr = fringe.get() # Dequeue from fringe.

        if curr == ship.button.cell: # There is a path from 🤖 to 🔘.
            # Build path:
            path = deque() # Create a stack.
            path.append(ship.button.cell) # Start from the goal and /recall/ steps to the initial cell.
            
            cell = ship.button.cell
            while cell != ship.bot.cell:
                cell = path[-1]
                if cell != prev[cell]: # This means we got to the initial cell.
                    path.append(prev[cell])
            
            # Execute bot movement and fire advancement by popping the entire path:
            while ship.bot.cell != ship.button.cell and len(path) > 0:
                if ship.bot.cell.on_fire:
                    return False
                
                ship.bot.cell = path.pop()
                print("...Bot moving to (", ship.bot.cell.x, ", ", ship.bot.cell.y, ")")
                # Advance fire.
                ship.advance_fire()
            
            return True
        
        # Check left to see if it is an open cell that is not the initial fire cell and has not been visited:
        if curr.x - 1 >= 0 and ship.grid[curr.x - 1][curr.y] != ship.initial_fire.cell and ship.grid[curr.x - 1][curr.y].is_open is True and ship.grid[curr.x - 1][curr.y] not in closed_set:
            # Add to fringe.
            fringe.put(ship.grid[curr.x - 1][curr.y])
            # Add to parent.
            prev[ship.grid[curr.x - 1][curr.y]] = curr
        # Check right:
        if curr.x + 1 < ship.d and ship.grid[curr.x + 1][curr.y] != ship.initial_fire.cell and ship.grid[curr.x + 1][curr.y].is_open is True and ship.grid[curr.x + 1][curr.y] not in closed_set:
            fringe.put(ship.grid[curr.x + 1][curr.y])
            prev[ship.grid[curr.x + 1][curr.y]] = curr
        # Check up:
        if curr.y + 1 < ship.d and ship.grid[curr.x][curr.y + 1] != ship.initial_fire.cell and ship.grid[curr.x][curr.y + 1].is_open is True and ship.grid[curr.x][curr.y + 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y + 1])
            prev[ship.grid[curr.x][curr.y + 1]] = curr
        # Check down:
        if curr.y - 1 >= 0 and ship.grid[curr.x][curr.y - 1] != ship.initial_fire.cell and ship.grid[curr.x][curr.y - 1].is_open is True and ship.grid[curr.x][curr.y - 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y - 1])
            prev[ship.grid[curr.x][curr.y - 1]] = curr
        
        # Mark as visited.
        closed_set.add(curr)
    
    return False

# Bot2 Helper Method
def run_bot2_bfs(ship):
    """
    Helper method used to run Bot2.
    It runs BFS to look for a shortest path where /every/ cell in the path is not a 🔥 cell.
    
    :return: shortest path from bot to button if it exists, or none otherwise.
    """
    fringe = Queue() # For BFS.
    closed_set = set() # Tracks visited cells.
    prev = {ship.bot.cell : ship.bot.cell} # Tracks parent and builds visited path.
    
    fringe.put(ship.bot.cell)
    
    while fringe.empty() is False:
        curr = fringe.get() # Dequeue from fringe.

        if curr == ship.button.cell: # There is a path from 🤖 to 🔘.
            # Build path:
            path = deque() # Create a stack.
            path.append(ship.button.cell) # Start from the goal and /recall/ steps to the initial cell.
            
            cell = ship.button.cell
            while cell != ship.bot.cell:
                cell = path[-1]
                if cell != prev[cell]: # This means we got to the initial cell.
                    path.append(prev[cell])
            path.pop() # Remove current ship.bot.cell from path.
            return path
    
        # Check left to see if it is an open cell that is not on fire and has not been visited:
        if curr.x - 1 >= 0 and ship.grid[curr.x - 1][curr.y].on_fire is False and ship.grid[curr.x - 1][curr.y].is_open is True and ship.grid[curr.x - 1][curr.y] not in closed_set:
            # Add to fringe.
            fringe.put(ship.grid[curr.x - 1][curr.y])
            # Add to parent.
            prev[ship.grid[curr.x - 1][curr.y]] = curr
        # Check right:
        if curr.x + 1 < ship.d and ship.grid[curr.x + 1][curr.y].on_fire is False and ship.grid[curr.x + 1][curr.y].is_open is True and ship.grid[curr.x + 1][curr.y] not in closed_set:
            fringe.put(ship.grid[curr.x + 1][curr.y])
            prev[ship.grid[curr.x + 1][curr.y]] = curr
        # Check up:
        if curr.y + 1 < ship.d and ship.grid[curr.x][curr.y + 1].on_fire is False and ship.grid[curr.x][curr.y + 1].is_open is True and ship.grid[curr.x][curr.y + 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y + 1])
            prev[ship.grid[curr.x][curr.y + 1]] = curr
        # Check down:
        if curr.y - 1 >= 0 and ship.grid[curr.x][curr.y - 1].on_fire is False and ship.grid[curr.x][curr.y - 1].is_open is True and ship.grid[curr.x][curr.y - 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y - 1])
            prev[ship.grid[curr.x][curr.y - 1]] = curr
        
        # Mark as visited.
        closed_set.add(curr)
    
    return None # There is no walkable path from 🤖 to 🔘.

# Bot2 Method
def run_bot2(ship):
    """
    Method used to run Bot2 via Breadth-First Search.

    :return: true if bot was able to reach button, or false otherwise.
    """
    # Execute bot movement and fire advancement by popping from each path once:
    while ship.bot.cell != ship.button.cell:
        if ship.bot.cell.on_fire:
            return False
        
        path = run_bot2_bfs(ship) # Find /current/ shortest path avoiding /current/ fire cells.
        if path is None:
            return False
        
        ship.bot.cell = path.pop() # Pop the first bot movement from /current/ shortest path.
        print("...Bot moving to (", ship.bot.cell.x, ", ", ship.bot.cell.y, ")")
        ship.advance_fire() # Advance fire.
    
    return True

# Bot3 Helper Method
def run_bot3_bfs(ship):
    """
    Helper method used to run Bot3.
    It runs BFS to look for a shortest path where /every/ cell in the path is not adjacent to a 🔥 cell.
    Only if it is unsuccessful, it then runs BFS again to look for a shortest path, ignoring whether or not the cells of the path are adjacent to a 🔥 cell.
    Bot3 prioritizes the "safer" path over the "risky" one, even if the "risky" one is shorter.

    :return: shortest path from bot to button if it exists, or none otherwise.
    """
    fringe = Queue() # For BFS.
    closed_set = set() # Tracks visited cells.
    prev = {ship.bot.cell : ship.bot.cell} # Tracks parent and builds visited path.
    
    fringe.put(ship.bot.cell)
    
    while fringe.empty() is False:
        curr = fringe.get() # Dequeue from fringe.

        if curr == ship.button.cell: # There is a path from 🤖 to 🔘, where /every/ cell in the path is not adjacent to a 🔥 cell.
            return prev
        
        # Check left to see if it is an open cell that is not on fire or near any fire and has not been visited:
        if curr.x - 1 >= 0 and ship.grid[curr.x - 1][curr.y].on_fire is False and ship.has_open_neighbors_on_fire(ship.grid[curr.x - 1][curr.y]) == 0 and ship.grid[curr.x - 1][curr.y].is_open is True and ship.grid[curr.x - 1][curr.y] not in closed_set:
            fringe.put(ship.grid[curr.x - 1][curr.y])
            prev[ship.grid[curr.x - 1][curr.y]] = curr
        # Check right:
        if curr.x + 1 < ship.d and ship.grid[curr.x + 1][curr.y].on_fire is False and ship.has_open_neighbors_on_fire(ship.grid[curr.x + 1][curr.y]) == 0 and ship.grid[curr.x + 1][curr.y].is_open is True and ship.grid[curr.x + 1][curr.y] not in closed_set:
            fringe.put(ship.grid[curr.x + 1][curr.y])
            prev[ship.grid[curr.x + 1][curr.y]] = curr
        # Check up:
        if curr.y + 1 < ship.d and ship.grid[curr.x][curr.y + 1].on_fire is False and ship.has_open_neighbors_on_fire(ship.grid[curr.x][curr.y + 1]) == 0 and ship.grid[curr.x][curr.y + 1].is_open is True and ship.grid[curr.x][curr.y + 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y + 1])
            prev[ship.grid[curr.x][curr.y + 1]] = curr
        # Check down:
        if curr.y - 1 >= 0 and ship.grid[curr.x][curr.y - 1].on_fire is False and ship.has_open_neighbors_on_fire(ship.grid[curr.x][curr.y - 1]) == 0 and ship.grid[curr.x][curr.y - 1].is_open is True and ship.grid[curr.x][curr.y - 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y - 1])
            prev[ship.grid[curr.x][curr.y - 1]] = curr
        
        # Mark as visited.
        closed_set.add(curr)
    
    # If we arrive at this line, it means that a "safe" path from 🤖 to 🔘 does not exist.
    # We redo BFS with less strict conditions.
    fringe = Queue() # Clear the queue.
    closed_set.clear() # Clear the set.
    prev.clear()
    prev = {ship.bot.cell : ship.bot.cell}
    fringe.put(ship.bot.cell)

    while fringe.empty() is False:
        curr = fringe.get() # Dequeue from fringe.

        if curr == ship.button.cell: # The shortest path from 🤖 to 🔘 has at least one cell in the path is adjacent to a 🔥 cell.
            return prev
        
        # Check left to see if it is an open cell that is not on fire and has not been visited:
        if curr.x - 1 >= 0 and ship.grid[curr.x - 1][curr.y].on_fire is False and ship.grid[curr.x - 1][curr.y].is_open is True and ship.grid[curr.x - 1][curr.y] not in closed_set:
            fringe.put(ship.grid[curr.x - 1][curr.y])
            prev[ship.grid[curr.x - 1][curr.y]] = curr
        # Check right:
        if curr.x + 1 < ship.d and ship.grid[curr.x + 1][curr.y].on_fire is False and ship.grid[curr.x + 1][curr.y].is_open is True and ship.grid[curr.x + 1][curr.y] not in closed_set:
            fringe.put(ship.grid[curr.x + 1][curr.y])
            prev[ship.grid[curr.x + 1][curr.y]] = curr
        # Check up:
        if curr.y + 1 < ship.d and ship.grid[curr.x][curr.y + 1].on_fire is False and ship.grid[curr.x][curr.y + 1].is_open is True and ship.grid[curr.x][curr.y + 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y + 1])
            prev[ship.grid[curr.x][curr.y + 1]] = curr
        # Check down:
        if curr.y - 1 >= 0 and ship.grid[curr.x][curr.y - 1].on_fire is False and ship.grid[curr.x][curr.y - 1].is_open is True and ship.grid[curr.x][curr.y - 1] not in closed_set:
            fringe.put(ship.grid[curr.x][curr.y - 1])
            prev[ship.grid[curr.x][curr.y - 1]] = curr

        closed_set.add(curr)
    
    return None # There is no walkable path from 🤖 to 🔘.

# Bot3 Method
def run_bot3(ship):
    """
    Method used to run Bot3 via Breadth-First Search.

    :return: true if bot was able to reach button, or false otherwise.
    """
    # Execute bot movement and fire advancement.
    while ship.bot.cell != ship.button.cell:
        if ship.bot.cell.on_fire:
            return False
        
        prev = run_bot3_bfs(ship)
        if prev is None:
            return False

        # Recall steps according to prev dictionary:
        path = deque() # Create a stack.
        path.append(ship.button.cell)
        cell = ship.button.cell # Start from the goal and /recall/ steps to the initial cell.
        while cell != ship.bot.cell:
            cell = path[-1]
            if ship.bot.cell != cell and cell != prev[cell]: # Do not include the cell 🤖 is currently in in the path.
                path.append(prev[cell])
        path.pop() # The top of the path stack is the current cell so we remove it first to reveal the next step 🤖 will take next.
        ship.bot.cell = path.pop()
        print("...Bot moving to (", ship.bot.cell.x, ", ", ship.bot.cell.y, ")")
        ship.advance_fire() # Advance fire.
    
    return True

# Bot4 Helper Method
def calculate_danger_factor(ship, cell):
    """
    Helper method used to run Bot4.
    It runs run_bot2_bfs on a copy of ship and moves around the bot and button positions to find a specific shortest path.
    It is used to calculate the danger path of f(n) by looking at g(n) and h(n).

    :return: f_n OR g(n) + h(n)
    """
    ship_copy1 = copy.deepcopy(ship)
    ship_copy2 = copy.deepcopy(ship)
    f_n = 0

    # Calculate g_n which is danger from bot to cell.
    ship_copy1.button.cell = cell
    g_n = run_bot2_bfs(ship_copy1)
    if g_n is not None:
        while len(g_n) > 0:
            g_n_cell = g_n.pop()
            value = ship_danger_factors.get(g_n_cell, 0) # If cell does not exist in dictionary, return 0.
            f_n += value
    
    # Calculate h_n which is danger from cell to button.
    ship_copy2.bot.cell = cell
    h_n = run_bot2_bfs(ship_copy2)
    if h_n is not None:
        while len(h_n) > 0:
            h_n_cell = h_n.pop()
            value = ship_danger_factors.get(h_n_cell, 0) # If cell does not exist in dictionary, return 0.
            f_n += value
    
    return f_n


# Bot4 Helper Method
def run_bot4_astar(ship):
    """
    Helper method used to run Bot4.
    It runs A* to look for an optimal path by prioritizing fringe based on f(n) = g(n) + h(n) where...
    f(n) is /total/ danger path from bot to button.
    g(n) is danger path from bot to some node n.
    h(n) is danger path from node n to button.

    :return: optimal path from bot to button if it exists, or none otherwise.
    """
    fringe = queue.PriorityQueue() # For A*.
    closed_set = set() # Tracks visited cells.
    prev = {ship.bot.cell : ship.bot.cell} # Tracks parent and builds visited path.

    fringe.put((0, ship.bot.cell))

    while fringe.empty() is False:
        f_n, curr = fringe.get() # Dequeue from fringe based on lowest danger factor.

        if curr == ship.button.cell: # There is a path from 🤖 to 🔘.
            # Build path:
            path = deque() # Create a stack.
            path.append(ship.button.cell) # Start from the goal and /recall/ steps to the initial cell.
            
            cell = ship.button.cell
            while cell != ship.bot.cell:
                cell = path[-1]
                if cell != prev[cell]: # This means we got to the initial cell.
                    path.append(prev[cell])
            path.pop() # Remove current ship.bot.cell from path.
            return path

        # Check left to see if it is an open cell that is not on fire and has not been visited:
        if curr.x - 1 >= 0 and ship.grid[curr.x - 1][curr.y].on_fire is False and ship.grid[curr.x - 1][curr.y].is_open is True and ship.grid[curr.x - 1][curr.y] not in closed_set:
            # Calculate f_n.
            f_n = calculate_danger_factor(ship, ship.grid[curr.x - 1][curr.y])
            # Add to fringe based on total danger of path /through/ this neighbor.
            fringe.put((f_n, ship.grid[curr.x - 1][curr.y]))
            # Add to parent.
            prev[ship.grid[curr.x - 1][curr.y]] = curr
        # Check right:
        if curr.x + 1 < ship.d and ship.grid[curr.x + 1][curr.y].on_fire is False and ship.grid[curr.x + 1][curr.y].is_open is True and ship.grid[curr.x + 1][curr.y] not in closed_set:
            f_n = calculate_danger_factor(ship, ship.grid[curr.x + 1][curr.y])
            fringe.put((f_n, ship.grid[curr.x + 1][curr.y]))
            prev[ship.grid[curr.x + 1][curr.y]] = curr
        # Check up:
        if curr.y + 1 < ship.d and ship.grid[curr.x][curr.y + 1].on_fire is False and ship.grid[curr.x][curr.y + 1].is_open is True and ship.grid[curr.x][curr.y + 1] not in closed_set:
            f_n = calculate_danger_factor(ship, ship.grid[curr.x][curr.y + 1])
            fringe.put((f_n, ship.grid[curr.x][curr.y + 1]))
            prev[ship.grid[curr.x][curr.y + 1]] = curr
        # Check down:
        if curr.y - 1 >= 0 and ship.grid[curr.x][curr.y - 1].on_fire is False and ship.grid[curr.x][curr.y - 1].is_open is True and ship.grid[curr.x][curr.y - 1] not in closed_set:
            f_n = calculate_danger_factor(ship, ship.grid[curr.x][curr.y - 1])
            fringe.put((f_n, ship.grid[curr.x][curr.y - 1]))
            prev[ship.grid[curr.x][curr.y - 1]] = curr

        # Mark as visited.
        closed_set.add(curr)
    
    return None # There is no walkable path from 🤖 to 🔘.

# Bot4 Method
def run_bot4(ship):
    """
    Method used to run Bot4 via MCTS and A*.

    :return: true if bot was able to reach button, or false otherwise.
    """
    # Run 50 simulations of fire advancement to calculate which cells are /most/ likely to catch on fire.
    for s in range(50):
        # Copy of ship.
        ship_copy = copy.deepcopy(ship)

        # Simulate fire advancement till bot or button catches on fire.
        while (ship_copy.bot.cell.on_fire is False or ship_copy.button.cell.on_fire is False):
            ship_copy.advance_fire()

        # Iterate /current/ fire cells and add to dictionary.
        for fire_cell in ship_copy.cells_on_fire:
            if fire_cell in ship_danger_factors:
                ship_danger_factors[fire_cell] += 1
            else:
                ship_danger_factors[fire_cell] = 1
    
    # Execute bot movement and fire advancement by popping from each path once:
    while ship.bot.cell != ship.button.cell:
        if ship.bot.cell.on_fire:
            return False
        
        path = run_bot4_astar(ship) # Find /current/ optimal path based on A*.
        if path is None:
            return False
        
        ship.bot.cell = path.pop() # Pop the first bot movement from /current/ optimal path.
        print("...Bot moving to (", ship.bot.cell.x, ", ", ship.bot.cell.y, ")")
        ship.advance_fire() # Advance fire.
    
    return True

# Main Method
def main():
    """
    Main Method used to run SpaceVessel.
    """
    # Get user input for spaceship specifications (size and flammability).
    print('Enter an integer D to define a (D x D) square grid layout of the Archaeopteryx space vessel:')
    d = int(input())
    print('Enter a decimal q between 0 and 1 to define the flammability of the Archaeopteryx space vessel:')
    q = decimal.Decimal(input())
    print('Enter which bot you want to run in the simulation (1, 2, 3, or 4):')
    bot_num = int(input())
    print('Enter the number of times to run the simulation:')
    times_to_run = int(input())

    # Tracks the number of successes.
    num_successes = 0
    # Tracks the number of failures.
    num_failures = 0

    # For-loop is used to run simulations several times, which will used as data for the graph in the write-up. 
    for index in range(times_to_run):
        # Initialize the spaceship.
        ship = Ship(d, q)

        # Generate random initial cell position.
        x = random.randint(0, d - 1)
        y = random.randint(0, d - 1)

        # Open random cell position on spaceship.
        ship.open_cell(x, y)

        # Iteratively create the path on grid layout.
        # While blocked cells with exactly one open neighbor exist, randomly open a cell from list.
        while (ship.blocked_cells_w_one_open_neighbor):
            cell_to_open_index = random.randint(0, len(ship.blocked_cells_w_one_open_neighbor) - 1)
            cell_to_open = ship.blocked_cells_w_one_open_neighbor.pop(cell_to_open_index)

            ship.open_cell(cell_to_open.x, cell_to_open.y)

        # Clean up dead-ends list and remove open cells that do not have exactly one open neighbor.
        for dead_end in ship.dead_ends[:]: # Iterate through a local copy of ship.dead_ends.
            if ship.has_single_open_neighbor(dead_end) is False:
                ship.dead_ends.remove(dead_end)

        # Loop through about half of the dead-ends in ship.dead_ends and randomly open /one/ of its blocked neighbors.
        for i in range(math.floor(len(ship.dead_ends) / 2)):
            cell_to_open_index = random.randint(0, len(ship.dead_ends) - 1)
            ship.open_dead_end(ship.dead_ends[cell_to_open_index])
        
        # Place bot on ship.
        ship.spawn_bot()
        # Place button on ship.
        ship.spawn_button()
        # Start fire on ship.
        ship.spawn_initial_fire()

        # Start simulation.
        print("*** STARTING SIMULATION ***")
        print("Bot Cell: (", ship.bot.cell.x, ", ", ship.bot.cell.y, ")")
        print("Button Cell: (", ship.button.cell.x, ", ", ship.button.cell.y, ")")
        print("Initial Fire Cell: (", ship.initial_fire.cell.x, ", ", ship.initial_fire.cell.y, ")")
        print(ship)

        if bot_num == 1:
            if run_bot1(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        if bot_num == 2:
            if run_bot2(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        if bot_num == 3:
            if run_bot3(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        if bot_num == 4:
            if run_bot4(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        
        print(ship)
    
    print("Number of successes: ", num_successes)
    print("Number of failures: ", num_failures)

# Main Driver
if __name__ == "__main__":
    main()