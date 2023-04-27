import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class Board():
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
        nest = self.size // 2
        direction = random.randint(1,7)
        returning_home = False
        self.ants.append([nest, nest, direction, returning_home])

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
            x = ant[0]
            y = ant[1]
            #Ant adds less pheromone on more saturated trails
            self.pheromones[x][y] -= ((self.tau / self.sauturation_concentration) * self.pheromones[x][y]) 

            #Ant adds normal amount of pheromones
            self.pheromones[x][y] += self.tau 

            #Ant adds more pheromone when returning to nest
            self.pheromones[x][y] += self.tau * ant[3]

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
        direction = ant[2]
        for i in range(direction - 1, direction + 2, 1):
            i = i % 8 
            x = ant[0] + self.possible_moves[i][0] 
            y = ant[1] + self.possible_moves[i][1]
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

    def follow(self, ant, nearby_pheromones):
        """
        Determines which trail a following ant will follow and updates its direction
            Parameters:
                ant (lst) : the ant to update
                nearby_pheromones (lst): the pheromone amount in the three cells in front of the ant
        """
        left, straight, right = nearby_pheromones

        #If trail ahead go stright
        if straight != 0.0:
            pass
        #Otherwise follow strongest trail
        elif left > right :
            ant[2] = (ant[2] + 1) % 8  
        elif right > left :
            ant[2] = (ant[2] - 1) % 8 

    def explore(self, ant):
        """
        Updates an exploring ant's direction
            Parameters:
                ant (lst) : the ant to update
        """
        prob_go_straight = 1 - 2 * sum(self.turning_kernel)
        turning_probabilities = [prob_go_straight] + self.turning_kernel
        turning_amount_choices = [0,1,2,3,4]
        turn_amount = random.choices(turning_amount_choices, weights=turning_probabilities, k=1)[0]
        turn_direction = random.randint(-1, 1) #left or right

        new_direction = (ant[2] + turn_amount * turn_direction + 8) % 8
        ant[2]  = new_direction

    def gather(self, ant, nearby_food):
        """
        Decrease food in field and send a gathering ant home 
            Parameters:
                ant (lst) : the ant to update
                nearby_food (lst): the food amount in the three cells in front of the ant
        """
        #Calculates where max nearby food is
        max_food_index = nearby_food.index(max(nearby_food)) - 1
        food_direction = (ant[2] + max_food_index) % 8 
        food_x = ant[0] + self.possible_moves[food_direction][0]
        food_y = ant[1] + self.possible_moves[food_direction][1]
        #removes 1 food from location
        self.food[food_x][food_y] -= 1
        #sets ant to return to the nest
        ant[3] = True

    def go_to_nest(self, ant):
        """
        Updates a ants direction to point towards nest
            Parameters:
                ant (lst) : the ant to update
        """
        nest = self.size // 2 
        x_direction_of_nest = np.sign(nest - ant[0])
        y_direction_of_nest = np.sign(nest - ant[1])
        ant[2] = self.possible_moves.index((x_direction_of_nest, y_direction_of_nest))

    def ant_at_nest(self, ant):
        """
        Updates and retuning ant's status if it is at the nest
            Parameters:
                ant (lst) : the ant to update
        """
        nest = self.size // 2 
        at_nest = (ant[0] == nest and ant[1] == nest)
        if ant[3] and at_nest:
            # sets a retuning ant at next to  to the nest
            ant[3] = False

    def turn_ants(self):
        """
        Updates ants directions 
        """
        explorers = 0
        followers = 0
        gatherers = 0 
        returners = 0 
        for ant in self.ants:
            nearby_pheromones = self.find_nearby_values(ant, self.pheromones)
            nearby_food = self.find_nearby_values(ant, self.food)
            self.ant_at_nest(ant)
            if ant[3]:
                self.go_to_nest(ant)
                returners += 1
            elif any(nearby_food):
                self.gather(ant, nearby_food)
                gatherers += 1
            elif self.ant_follows_trail(nearby_pheromones):
                self.follow(ant, nearby_pheromones)
                followers += 1
            else:
                self.explore(ant)
                explorers += 1

        return explorers, followers, gatherers, returners

    def move_ants(self):
        """
        Updates ants positions forward in whichever direction it is facing
        """
        for ant in self.ants:
            ant[0] += self.possible_moves[ant[2]][0]
            ant[1] += self.possible_moves[ant[2]][1]

    def clean(self):
        """
        Deletes ants which have wandered off board
        """
        for ant in self.ants.copy():
            if not self.is_in_grid(ant[0], ant[1]):
                self.ants.remove(ant)

    def step(self):
        """
        Simulates a single timestep (second)
        """
        self.release_ant()
        self.deposit()
        self.evaporate()
        explorers, followers, gatherers, returners= self.turn_ants()
        self.move_ants()
        self.clean()
        return explorers, followers, gatherers, returners

    def run(self, minutes):
        """
        Runs the model for a specified number of minutes
        """
        for minute in range(minutes): 
            for seconds in range(60):
                explorers, followers, gatherers, returners = self.step()
            print(minute)   
            print("explorers = " + str(explorers))
            print("followers = " + str(followers))
            print("gatherers = " + str(gatherers))
            print("returners = " + str(returners))

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
            ant_xs.append((ant[0] + .5))
            ant_ys.append((ant[1] + .5))
        plt.pcolormesh(pheromones, cmap='Greys')
        plt.pcolormesh(food, cmap='jet')
        cmap = plt.cm.get_cmap('jet')
        cmap.set_bad(alpha=0)

        # plt.scatter(ant_xs, ant_ys) #this line is still in development
        plt.show()

model = Board()
model.run(minutes = 60)
model.draw()


