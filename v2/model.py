import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from ant import Ant

class Board():
    """The model containing the lattice and a set of ants
    Attributes:
    size : int
        the width and height of the square lattice 
    possible_moves : lst of tuples
        a list of all possible moves
    deposition_rate  : int 
        how much pheramone an ant deposits per time step
    min_phi : int (between 0 and 255)
        the minimum probability that an ant will follow a trail
    delta_phi : int 
        the amount that the proability an ant will follow a trail increase per unit pheramone
    sautration_concentration: int
        the amount of pheramone above which an ant cannot differentiate.  
    turning_kernal : list of floats
        the proabilitlies that an exploring ant will make a specfic turn

    pheromone : pandas Dataframe
        a lattice of pheromone values on board
    food : pandas Dataframe
        a lattice of food values on board
    ant : lst of Ants
        a list of all Ants on board 
    """
    def __init__(
        self, 
        size = 256, 
        deposition_rate=8,
        min_phi = 247,
        delta_phi = 0,
        sauturation_concentration=100,
        turning_kernel = [.36, .047, .008, .004],
        ):

        #constant variables
        self.size = size
        self.possible_moves = [(0, 1), (1, 1), (1,0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.tau = deposition_rate
        self.min_phi = min_phi
        self.delta_phi = delta_phi
        self.sauturation_concentration = sauturation_concentration
        self.turning_kernel = turning_kernel

        #variable variables
        self.pheromones = pd.DataFrame(np.zeros((size, size), dtype=np.int32))
        self.food = pd.DataFrame(np.zeros((size, size), dtype=np.int32))
        self.ants = []

    def is_in_grid(self, x , y):
        """
        Returns true if the posotion is in the grid and false if else
            Parameters:
                x (int) : x position
                y (int) : y position

            Returns:
                (boolean)

        *Note:If x and y are not given they are assumed to be that of the ant's positons*
        """
        return  (x < self.size and y < self.size and x >= 0 and y >= 0)

    def release_ant(self):
        """
        Releases an ant from the nest
        """
        new_ant = Ant((self.size // 2))
        self.ants.append(new_ant)

    def evaporate(self): 
        """
        Subtracts a set amount of pheramones from all cells in pheromones
        """
        self.pheromones.where(self.pheromones == 0, self.pheromones - 1)

    def deposit(self):
        """
        Adds of pheramones to the cell where the ant is presents
        """
        for ant in self.ants:
            x = ant.x
            y = ant.y
            #Ant adds less pheromone on more saturated trails
            self.pheromones[x][y] -= ((self.tau / self.sauturation_concentration) * self.pheromones[x][y]) 

            #Ant adds normal amount of pheromones
            self.pheromones[x][y] += self.tau 

            #Ant adds more pheromone when returning to nest
            self.pheromones[x][y] += ant.food_seen

    def add_food(self, food_locations):
        """
        Finds the values of the cells adjacent to the ant
            Parameters:
                food (dict) : 
                    keys -> locations in (x,y) form
                    vals -> amount of food to add
        """
        for location, amount in food_locations.items():
            x,y = location 
            self.food[x][y] = amount 

    def find_nearby_values(self, ant, dataframe):
        """
        Finds the values of the cells adjacent to the ant
            Parameters:
                ant (lst) : the ant to check near
                dataframe (df) : the dataframe to check
            Returns
                values (lst of floats) : the values of the adjecent cells
        """
        values = []
        for i in range(ant.direction - 1, ant.direction + 2, 1):
            i = i % 8 
            x = ant.x + self.possible_moves[i][0] 
            y = ant.y + self.possible_moves[i][1]
            is_in_grid = self.is_in_grid(x, y)
            if is_in_grid:
                values.append(dataframe[x][y])
            else: 
                values.append(0.0)
        return values

    def ant_follows_trail(self, nearby_pheromones):
        """
        Determines if ant explores or follows a trail at any one time step.
            Parameters:
                nearby_pheromones (lst): the pheromone amount in the three cells in front of the ant
            Returns
                True if ant will follow the trail
        """
        if (nearby_pheromones[1] == 0) and (nearby_pheromones[0] == nearby_pheromones[2]):
            return False
        else:
            #Ensures the concentration input is not greater than the saturation concentration
            concentration = min(max(nearby_pheromones), self.sauturation_concentration) 
            probability = (self.min_phi + self.delta_phi * concentration)/ 256
            return random.random() < probability

    def update_ants(self):
        """
        Updates ants directions and position 
        """
        explorers = 0
        followers = 0
        gatherers = 0 
        returners = 0 
        for ant in self.ants:
            nearby_pheromones = self.find_nearby_values(ant, self.pheromones)
            nearby_food = self.find_nearby_values(ant, self.food)
            ant.ant_at_nest()

            if ant.food_seen:
                ant.go_to_nest(self.possible_moves)
                returners += 1
            elif any(nearby_food):
                ant.gather(nearby_food, self.food, self.possible_moves)
                gatherers += 1
            elif self.ant_follows_trail(nearby_pheromones):
                ant.follow(nearby_pheromones)
                followers += 1
            else:
                ant.explore(self.turning_kernel)
                explorers += 1

            ant.x += self.possible_moves[ant.direction][0]
            ant.y += self.possible_moves[ant.direction][1]
        return explorers, followers, gatherers, returners

    def clean(self):
        """
        Deletes ants which have wandered off board
        """
        for ant in self.ants.copy():
            if not self.is_in_grid(ant.x, ant.y):
                self.ants.remove(ant)

    def step(self):
        """
        Simulates a single timestep (second)
        """
        self.release_ant()
        self.deposit()
        self.evaporate()
        self.update_ants()
        self.clean()

    def run(self, minutes, food_locations):
        """
        Runs the model for a specified number of minutes
        """
        self.add_food(food_locations)
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(food_locations.keys())
        for minute in range(minutes): 
            for seconds in range(60):
                self.step()
            print(minute)   
            food_data = self.collect_food_data(food_locations)
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(food_data.values())

    def draw(self):
        """
        Draws the pheromones trails and the food
        """
        ant_xs = []
        ant_ys = []
        center_x, center_y = self.pheromones.shape[0] // 2, self.pheromones.shape[1] // 2
        pheromones = self.pheromones.copy()
        food = self.food.copy()
        food[food == 0] = np.nan
        for ant in self.ants:
            ant_xs.append((ant.x + .5))
            ant_ys.append((ant.y + .5))
        plt.pcolormesh(pheromones, cmap='Greys')
        plt.pcolormesh(food, cmap='jet')
        cmap = plt.cm.get_cmap('jet')
        cmap.set_bad(alpha=0)

        # plt.scatter(ant_xs, ant_ys) #this line is still in development
        plt.show()

    def collect_food_data(self, food_locations):
        """
        Finds the values of the cells adjacent to the ant
            Parameters:
                food (dict) : 
                    keys -> locations in (x,y) form
                    vals -> amount of food to add
        """
        current_food_at_locations = {}
        for location, amount in food_locations.items():
            x,y = location 
            current_food_at_locations[location] = self.food[x][y]
        return current_food_at_locations

            
model = Board()
food_locations ={(192,128) : 100, (64,128) : 10}
model.run(minutes = 60, food_locations = food_locations)
model.draw()


