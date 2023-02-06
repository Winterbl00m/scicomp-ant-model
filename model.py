import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from time import sleep
import matplotlib.cm as cm
# import matplotlib.pyplot.clf as clear_output

        # self.min_phi = 0 
        # self.delta_phi = 0
        # self.sauration_concentration  = 0 

class Ant:
    def __init__(self, starting_x, starting_y, turning_kernel, min_phi, delta_phi, sauturation_concentration):
        self.turning_kernel = turning_kernel
        self.min_phi = min_phi
        self.delta_phi = delta_phi
        self.sauturation_concentration = sauturation_concentration
        self.last_x = starting_x
        self.last_y = starting_y
        self.x = starting_x
        self.y = starting_y

        self.directions = [(0, 1), (1, 1), (1,0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.direction_index = random.randint(1,7)
        self.is_lost =  True
        self.adjacent_cells_values = []


    def is_in_grid(self, grid, x = None, y = None):
        """
        Returns true if the posotion is in the grid and flase if else
        """
        if x == None:
            x = self.x
        if y == None:
            y = self.y
        return  (x < grid.shape[0] and y < grid.shape[1] and x >= 0 and y >= 0)

    def find_adjacnet_cells(self, grid):
        cells = []
        for direction in self.directions:
            x = self.x + direction[0]
            y = self.y + direction[1]
            cells.append((x,y))
        return cells

    def find_adjacnet_cells_values(self, grid):
        cells = self.find_adjacnet_cells(grid)
        values = []
        for (x,y) in cells:
            is_last_position = (x == self.last_x and y == self.last_y)
            if (self.is_in_grid(grid, x, y) and not is_last_position):
                value = grid[x][y]
                values.append(value)
            else: 
                values.append(0.0)
        return values

    def move(self):
        """
        Updates an ant's position forward in whichever direction it is facing
        """
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.directions[self.direction_index][0]
        self.y += self.directions[self.direction_index][1]

    def explore(self):
        """
        Updates an exploring ant's position and direction
        """
        self.direction_index = self.random_turn()

    def random_turn(self):
        """
        Updates an exploring ant's direction
        """
        turning_amount_choices = [1,2,3,4]
        turn_amount = random.choices(turning_amount_choices, weights=self.turning_kernel, k=1)[0]
        turn_direction = random.randint(-1, 1) #left or right
        new_direction = self.direction_index + turn_amount * turn_direction
        new_direction_index = (8 + new_direction) % 8  #translates our new_direction into an index between 0-7
        return new_direction_index


    def follow(self):
        """
        Updates an trail following ant's position and direction
        """
        trails_directions = [i for i, e in enumerate(self.adjacent_cells_values) if e != 0.0]
        if len(trails_directions) == 1:
            trail_direction_index  = trails_directions[0]
            self.direction_index = trail_direction_index
        else: 
            self.fork(trails_directions)

    def fork(self, trails_directions):
        """
        Handles case of more than one trail near the ant
        """
        strongest_trails_directions = [i for i, e in enumerate(self.adjacent_cells_values) if e == max(self.adjacent_cells_values)]

        if self.direction_index in trails_directions:
            self.direction_index = self.direction_index

        elif (len(strongest_trails_directions) > 1):
            self.is_lost = True
            self.explore()

        else: 
            self.direction_index = strongest_trails_directions[0]



    def near_trail(self):
        """
        Return true if the ant is near trail and false if not
        """
        return np.any(self.adjacent_cells_values)

    def follows_trail(self):
        """
        Determines if ant explores or follows a trail at any one time step.

        Returns True if ant will follow the trail
        """

        trail_concentration = max(self.adjacent_cells_values)
        probability = self.min_phi / 256
        return random.random() < probability

class Model:
    def __init__(self):
        self.ants = set()
        self.grid = pd.DataFrame(np.zeros((100, 100))) 

        self.evaporation_rate = 1 
        self.tau = 8

        self.min_phi = 255
        self.delta_phi = 0
        self.sauturation_concentration = 0
        self.turning_kernel = [.36, .047, .008, .004]


    def draw(self):
        """
        Draws the Grid
        """
        plt.pcolormesh(self.grid, cmap='Greys')
        plt.show()


    def deposit(self, ant):
        """
        adds a set amount(tau) of pheramones to all cells where ants are present
        """

        x = ant.x
        y = ant.y
        self.grid[x][y] += self.tau

    def evaporate(self): 
        """
        Subtracts a set amount of pheramones from all cells in grid
        """
        for i in range(self.grid.shape[0]): #iterate over rows
            for j in range(self.grid.shape[1]): #iterate over columns
                self.grid[i][j] = max(self.grid[i][j] - self.evaporation_rate, 0)


    def update_ants(self):
        """
        Updates an all ants positions and directions
        """
        num_followers = 0
        num_lost = 0

        for ant in self.ants.copy():
            ant.adjacent_cells_values = ant.find_adjacnet_cells_values(self.grid)

            if ant.near_trail():
                ant.is_lost = not ant.follows_trail()

            if ant.is_lost:
                ant.explore()
                num_lost += 1
            else:
                ant.follow()
                num_followers += 1

            if (not ant.is_in_grid(self.grid)):
                self.ants.remove(ant)
            else:
                self.deposit(ant)

            ant.move()


        return num_followers, num_lost


    def release_ant(self):
        """
        Release a new ant from the hive
        """
        starting_x, starting_y = self.grid.shape[0] // 2, self.grid.shape[1] // 2
        ant = Ant(starting_x, starting_y, self.turning_kernel, self.min_phi, self.delta_phi, self.sauturation_concentration)
        self.ants.add(ant)


    def step(self):
        """
        Simulates one time step
        """ 
        self.release_ant()
        self.evaporate()
        F, L = self.update_ants()
        print("F = " + str(F))
        print("L = " + str(L))
        # self.draw()      

model = Model()

for i in range(10000):
    print(i)
    model.step()
model.draw()