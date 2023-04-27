import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from ant import Ant

class Model:
    """The model containing the lattice and a set of ants

    Attributes:
    size : int
        the width and height of the square lattice 
    tau  : int 
        how much pheramone an ant deposits per time step
    min_phi : int (between 0 and 255)
        the minimum probability that an ant will follow a trail
    turning_kernal : list of floats
        the proabilitlies that an exploring ant will make a specfic turn
    delta_phi : int 
        the amount that the proability an ant will follow a trail increase per unit pheramone
    sautration_concentration: int
        the amount of pheramone above which an ant cannot differentiate. 
    """
    def __init__(self, 
        size, 
        tau, 
        min_phi, 
        turning_kernel, 
        delta_phi = 0, 
        sauturation_concentration = 1,
        food_locations = [[0,0,0]],
        k = 10):

        self.ants = set()
        self.pheromones = pd.DataFrame(np.zeros((size, size))) 
        self.food = pd.DataFrame(np.zeros((size, size))) 
        self.food_locations = food_locations
        self.add_food(food_locations)

        self.evaporation_rate = 1 
        self.tau = tau

        self.min_phi = min_phi
        self.delta_phi = delta_phi
        self.sauturation_concentration = sauturation_concentration
        self.turning_kernel = turning_kernel

        self.food_collected = 0
        self.k = k 

    def add_food(self, food_locations):
        for location in food_locations:
            x = location[0]
            y = location[1]
            amount = location[2]
            self.food[x][y] = amount

    def draw(self):
        """
        Draws the pheromones
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


    def deposit(self):
        """
        adds a set amount(tau) of pheramones to the cell where the ant is present
            Parameters:
                ant (Ant) : the ant which is depositing the pheramones
        """
        for ant in self.ants.copy():
            if (ant.is_in_grid(self.pheromones)):
                x = ant.x
                y = ant.y
                self.pheromones[x][y] += self.tau - (self.tau / self.sauturation_concentration) * self.pheromones[x][y] 
            else:
                self.ants.remove(ant)

    def evaporate(self): 
        """
        Subtracts a set amount of pheramones from all cells in pheromones
        """
        self.pheromones.where(self.pheromones == 0, self.pheromones - self.evaporation_rate)


    def update_ants(self):
        """
        Updates an all ants positions and possible_moves
        """
        explorers = 0
        followers = 0
        gatherers = 0 
        returners = 0 

        for ant in self.ants:
            if not ant.is_in_grid(self.pheromones):
                self.ants.remove(ant)
            else:
                ant.adjacent_cells_pheromones = ant.find_adjacnet_cells_values(self.pheromones)
                ant.nearby_food = ant.smell_nearby_food(self.food)
                ant.mode = ant.determine_mode(self.food)

                if ant.mode == "explore":
                    ant.explore()
                    explorers += 1
                elif ant.mode == "follow":
                    ant.follow()
                    followers += 1
                elif ant.mode == "gather":
                    ant.gather(self.food, 10)
                    gatherers += 1
                else: 
                    ant.go_home(self.food)
                    returners += 1

                ant.move()
        return explorers, followers, gatherers, returners

    def release_ant(self):
        """
        Release a new ant from the hive
        """
        starting_x, starting_y = self.pheromones.shape[0] // 2, self.pheromones.shape[1] // 2
        ant = Ant(self.pheromones.shape[0], self.turning_kernel, self.min_phi, self.delta_phi, self.sauturation_concentration, self.k)
        self.ants.add(ant)


    def step(self):
        """
        Simulates one time step
        """ 
        self.release_ant()
        self.deposit()
        self.evaporate()
        explorers, followers, gatherers, returners = self.update_ants()
        # print("explorers = " + str(explorers))
        # print("followers = " + str(followers))
        # print("gatherers = " + str(gatherers))
        # print("returners = " + str(returners))

    def save(self):
        """
        Saves the data in the model to csv's
        """
        self.pheromones.to_csv("pheromones.csv")
        ant_xs = []
        ant_ys = []
        for ant in self.ants:
            ant_xs.append((ant.x + .5))
            ant_ys.append((ant.y + .5))
        ant_positions = pd.DataFrame({'x':ant_xs, 'y':ant_xs})
        ant_positions.to_csv("ant_positions.csv")



    def run(self, minutes):
        for minute in range(minutes): 
            for seconds in range(60):
                model.step()
                for i, (x, y, last) in enumerate(self.food_locations): 
                    current = self.food[x][y]
                    self.food_locations[i][2] = current
            print(self.food_locations)


size = 256
tau = 8
min_phi = 247
turning_kernel = [.36, .047, .008, .004]
food_locations =[[38, 38, 1000]]
model = Model(size, tau, min_phi, turning_kernel, 0, tau, food_locations, k = 2)
mins = 60


model.run(1)
model.draw()

for ant in model.ants:
    print(ant.nearby_food)



