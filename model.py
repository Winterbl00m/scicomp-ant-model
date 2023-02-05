import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from time import sleep
# import matplotlib.pyplot.clf as clear_output

        # self.min_phi = 0 
        # self.delta_phi = 0
        # self.sauration_concentration  = 0 

class Ant:
    def __init__(self, grid, is_lost = True):
        self.last_x = grid.shape[0] // 2
        self.last_y = grid.shape[1] // 2
        self.x = grid.shape[0] // 2
        self.y = grid.shape[1] // 2
        self.directions = [(0, 1), (1, 1), (1,0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.direction_index = random.randint(1,7)
        self.is_lost =  is_lost
        self.adjacent_cells_values = self.find_adjacnet_cells_values(grid)
        self.turning_kernel = [.36, .047, .008, .004]

    def is_in_grid(self, grid, x = None, y = None):
        """
        Returns true if the posotion is in the grid and flase if else
        """
        if x == None:
            x = self.x
        if y == None:
            y = self.y
        return  (x != grid.shape[0] and y != grid.shape[1] and x >= 0 and y >= 0)

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
            else : 
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
        self.direction_index = self.turn_explore()
        self.move()

    def turn_explore(self):
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
        trail_direction_indexs = [i for i, e in enumerate(self.adjacent_cells_values) if e != 0.0]
        if len(trail_direction_indexs) == 1:
            trail_direction_index  = trail_direction_indexs[0]
            self.direction_index = trail_direction_index
            self.move()
        else: 
            self.fork(trail_direction_indexs)


    def fork(self, trail_direction_indexs):
        """
        Handles case of more than one trail near the ant
        """
        #TODO implement this 
        self.is_lost = True
        self.explore()

    def near_trail(self):
        """
        Return true if the ant is near trail and false if not
        """
        return np.any(self.adjacent_cells_values)



class Model:
    def __init__(self):
        self.ants = set()
        self.grid = pd.DataFrame(np.zeros((20, 20)))

        self.evaporation_rate = 0 
        self.tau = 10 


    def draw(self):
        """
        Draws the Grid
        """
        plt.pcolormesh(self.grid)
        plt.title('matplotlib.pyplot.pcolormesh() function Example', fontweight ="bold")
        plt.show()


    def deposit(self):
        """
        adds a set amount(tau) of pheramones to all cells where ants are present
        """
        for ant in self.ants:
            x = ant.x
            y = ant.y
            # print("depositing " + str(self.tau) + "at " + str(x) + str(y))
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
        for ant in self.ants.copy():
            ant.adjacent_cells_values = ant.find_adjacnet_cells_values(self.grid)

            if ant.is_lost:
                ant.explore()
                # print("exloring ant is at " + str(ant.x) + "," + str(ant.y))
                
            else:
                # print("following ant is at " + str(ant.x) + "," + str(ant.y))
                # print("Adjacents cells are " + str(ant.find_adjacnet_cells(self.grid)))
                # print("near_trail " + str(ant.near_trail()))
                ant.follow()

            if (not ant.is_in_grid(self.grid)):
                self.ants.remove(ant)


    def release_ant(self, is_lost):
        """
        Release a new ant from the hive
        """
        ant = Ant(self.grid, is_lost)
        self.ants.add(ant)


    def step(self):
        """
        Simulates one time step
        """ 
        # self.release_ant()
        self.evaporate()
        self.update_ants()
        self.deposit()
        # self.draw()      

model = Model()
model.release_ant(True)
model.step()
model.draw()

model.release_ant(False)
for i in range(5):
    model.step()
    model.draw()
