import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from time import sleep
# import matplotlib.pyplot.clf as clear_output



class Ant:
    def __init__(self, grid):
        self.last_x = grid.shape[0] // 2
        self.last_y = grid.shape[1] // 2
        self.x = grid.shape[0] // 2
        self.y = grid.shape[1] // 2
        self.directions = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1),(1, -1), (1, 0), (1, 1)]
        self.direction_index = random.randint(1,7)
        self.is_lost =  True
        self.min_phi = 0 
        self.delta_phi = 0
        self.sauration_concentration  = 0 

    def explore(self):
        """
        Updates an exploring ant's position and direction
        """
        self.direction_index = self.turn_explore()
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.directions[self.direction_index][0]
        self.y += self.directions[self.direction_index][1]

    def follow(self):
        """
        Updates an trail following ant's position and direction
        """
        pass

    def turn_explore(self):
        """
        Updates an exploring ant's direction
        """
        turning_kernel = [.36, .047, .008, .004]
        turning_amount_choices = [1,2,3,4]
        turn_amount = random.choices(turning_amount_choices, weights=turning_kernel, k=1)[0]
        turn_direction = random.randint(-1, 1)
        new_direction = self.direction_index + turn_amount * turn_direction
        new_direction_index = (8 + new_direction) % 8  #translates our new_direction into an index between 0-7
        print(self.direction_index, new_direction_index)
        return new_direction_index



    def turn_follow(self):
        """
        Updates an trail following ant's  direction
        """
        pass

    def near_trail(self):
        """
        Return true if the ant is near trail and false if not
        """
        pass 

class Model:
    def __init__(self):
        self.ants = set()
        self.grid = pd.DataFrame(np.zeros((100, 100)))
        self.evaporation_rate = 0 
        self.tau = 10 


    def draw(self):
        """
        Draws the Grid
        """
        plt.pcolormesh(self.grid)
        plt.title('matplotlib.pyplot.pcolormesh() function Example', fontweight ="bold")
        plt.show()

    def animate(self, frames, interval=None, step=None):
        """Animate the automaton.
        
        frames: number of frames to draw
        interval: time between frames in seconds
        iters: number of steps between frames
        """
        if step is None:
            step = self.step
            
        quad = plt.pcolormesh(self.grid)

        plt.ion()
        plt.show()
        try:
            for i in range(frames):
                step()
                quad.set_array(self.grid)
                # plt.title('Phase: %.2f'%phase)
                plt.draw()
                if interval:
                    sleep(interval)
        except KeyboardInterrupt:
            pass

        plt.ioff()

    def deposit(self):
        """
        adds a set amount(tau) of pheramones to all cells where ants are present
        """
        for ant in self.ants:
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
        for ant in self.ants.copy():
            if ant.is_lost:
                ant.explore()
            else:
                ant.follow()
            if (ant.x == self.grid.shape[0] or ant.y == self.grid.shape[1] or ant.x < 0 or ant.y < 0):
                self.ants.remove(ant)

    def release_ant(self):
        """
        Release a new ant from the hive
        """
        ant = Ant(self.grid)
        self.ants.add(ant)


    def step(self):
        """
        Simulates one time step
        """ 
        # print(self.grid)
        # self.release_ant()
        self.evaporate()
        self.update_ants()
        self.deposit()
        # self.draw()      

model = Model()
model.release_ant()
for i in range(20):
    model.step()

model.draw()

# model.animate(frames=10, interval=1)
