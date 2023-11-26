# 🛸 SpaceVessel
CS440: Project 1

SpaceVessel is an AI-powered Pathfinder Game taking place on the space vessel **_Archaeopteryx_**. Within the game, a bot named **_Juniper_** is tasked with ensuring the safety of the spacecraft during the crew's extended hibernation. An unexpected fire breaks out on the ship, requiring Juniper to press a button to activate the fire suppression system. However, with each movement made by Juniper, the fire spreads unpredictably, influenced by the flammability of the ship.

Can Juniper get to the button in time?! :robot:

# :space_invader: SpaceVessel Functions

## User Input

First, the user needs to set the parameters for the Archaeopteryx by specifying its size and flammability. The vessel size, denoted by **_D_**, is a square grid layout with dimensions (D x D), where D is any valid integer. The vessel flammability, denoted by **_q_**, ranges from 0 to 1 (1 being the highest flammability), where q is any valid decimal.

Following this, the user is required to deploy Juniper under specific configurations. Juniper offers four settings─namely Bot1, Bot2, Bot3, and Bot4. Each setting provides a distinct path to the button, with unique specifications.

Finally, the system allows for the execution of multiple simulations, wherein a selected bot navigates the ship to find the button. This functionality is designed for data collection and performance evaluation of the four Juniper settings. The simulations involve running 100 scenarios on a (50 x 50) grid, with the flammability parameter q varying from 0 to 1 in increments of 0.05. Using this data, we are able to expand on the flaws of each setting, the pros of each setting, why the bot fails given certain vessel conditions, and how to construct a new _ideal_ setting for Juniper to return the _most_ success.

## Generating the Vessel

Using values **_D_** and **_q_**, we generate a unique layout of the ship with walls, hallways, and dead-ends. First, we create a (D x D) square grid layout of "blocked" cells. We denote the _neighbors_ of a cell as the adjacent cells in the up/down/left/right direction. Diagonal cells are _not_ considered neighbors. Next, we "open" a random blocked cell on the grid. Then, we iteratively do the following:
* Find the _currently_ blocked cells that have exactly one open neighbor.
* Of these blocked cells with exactly one open neighbor, we "open" a random blocked cell.
* Repeat until you can no longer do so.

Finally, we identify all cells that are dead-ends (open cells with one open neighbor). For approximately half these dead-end cells, we "open" one of the closest neighbors of a random dead-end cell. This will be our vessel!

Note: 🔒 denotes cells that are blocked (Juniper cannot go into these cells), 🤖 denotes Juniper's current location on the ship, 🔥 denotes cells on fire.
<p align="center">
<img src="https://github.com/jasmeanfernando/SpaceVessel/assets/98361155/19db96a6-551d-4e90-be83-23ec127c6bba" alt="Vessel" title="Vessel">
</p>

## Generating the Simulation

We now begin our simulation!

At a random open cell, we spawn Juniper and an initial fire. At every time step, the fire has the ability to spread from its cell to adjacent open cells (the fire cannot spread to blocked cells). The fire spreads according to the following rules: At each time step, a non-burning open cell catches on fire with the probability 1 − (1 − q)<sup>K</sup> where **_q_** is the flammability of the vessel and **_K_** is the number of currently burning neighbors of this cell. Depending on the flammability and how big the fire is, the fire can spread to _multiple_ open cells.

Juniper's task is to map a path to the button while avoiding the fire using different strategies (via the setting of the Juniper)! At each time step, the following happens in sequence:
* Juniper decides which neighboring open cell to move to.
* The bot moves to that neighbor.
* If the bot enters the button cell─the button is pressed, the fire is put out, and the task is completed.
* Otherwise, the fire advances.
* If at any time step, the fire spreads to the button or the bot, the task has failed!

## Bot1

This setting plans the _quickest_ path to the button, avoiding only the _initial_ fire cell, and then executes that plan. The spread of the fire is completely ignored. This setting utilizes a Depth-First Search from Juniper's cell to the button.

## Bot2

This setting plans the _shortest_ path to the button at every time step, avoiding all current fire cells, and then executes that plan. Unlike Bot1, this setting is continuously changing its path depending on the spread of the fire. This setting utilizes a Breadth-First Search from Juniper's cell to the button.

## Bot3

This setting plans the _shortest_ path to the button at every time step, avoiding all current fire cells AND any cells adjacent to current fire cells, and then executes that plan. If there is no such path, it plans the shortest path to the button based on current fire cells, and then executes the next step in that plan. Unlike Bot2, this setting is continuously changing its path depending on the spread of the fire and cells _likely_ to catch on fire in the next time step. This setting utilizes a Breadth-First Search from Juniper's cell to the button.

## Bot4

This setting is a setting of its own design. Bot4 utilizes a search algorithm that combines the **Monty Carlo Tree Search** and **𝐴-Star Algorithm** in order to map the most optimal path from Juniper's initial cell to the button cell while avoiding current fire cells.

According to the ship's specifications, every time the bot moves, the fire has a chance to spread to nearby open cells. This chance is calculated by 1 − (1 − q)<sup>K</sup> enforced by a randomized threshold (since fire is meant to be unpredictable).

First, we run MCTS on this setting to take into account the danger factor of a cell, meaning how likely the fire will spread into that cell. We calculate this by running 50 simulations on a _copy_ of the ship where the fire spreads randomly until it reaches the bot or the button. Each time a cell catches on fire, we increment its danger factor. The danger factor of all individual cells will be held in a global dictionary where key = cell and value = number of times the cell caught on fire. At the most, a cell could have a danger factor of 50. After the global dictionary is populated with the danger factor of each open cell of the ship, we are going to continuously run A-Star to search for an optimal path from the bot to the button.

𝐴-Star is a search algorithm whose pseudocode is similar to a Breadth-First Search, where it utilizes a priority queue rather than a regular queue. The fringe is based on the total danger from the bot to the button through a given node n, f(n) = g(n) + h(n). So, f(n) is the estimated total danger path from the initial bot cell to the button cell, g(n) is the danger path from the initial bot cell to a specified cell n, and h(n) is the estimated danger path from the specified cell n to the button cell. All three paths of this expression map an optimal path while avoiding current fire cells. Danger path is the summation of the danger factors of all cells in a particular path.

Using a priority of f(n), this setting is able to make informed decisions about which cells to explore next in a search space. Cells are added to the fringe according to f(n) where the cell with the least danger path is dequeued first.

<p align="center">
<img src="https://github.com/jasmeanfernando/SpaceVessel/assets/98361155/840282f2-4a38-4ade-bfb3-88e68cda170e" alt="Vessel" title="Vessel">
</p>

