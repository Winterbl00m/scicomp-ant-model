import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class Ant:
    """
    An ant agents who will form trails

    Attributes:
    min_phi : int (between 0 and 255)
        the minimum probability that an ant will follow a trail
    turning_kernal : list of floats
        the proabilitlies that an exploring ant will make a specfic turn
    delta_phi : int 
        the amount that the proability an ant will follow a trail increase per unit pheramone
    sautration_concentration: int
        the amount of pheramone above which an ant cannot differentiate. 
    last_x : int
        the x position the ant was in on the last time step
    last_y : int 
        the y position the ant was in on the last time step
    x : int
        the x position the ant is in
    y : int 
        the y position the ant is in
    possible_moves : list of tuples in form (delta_x, delta_y)
        a list of all possible changes in an ants position in one time step
    direction : int (0-7)
        the direction that an ant is pointing with 0 being "north", 1 being"NE", 2 being "E", etc. 
    is_lost : boolean
        true if ant is lost (exploring) and false if not (following a trail)

    adjacent_cells_values : list of floats
        the pheramone concentration in the adjecent cells
        *Note: values are in directional order 
        (ex. the value at index = 0 is the phermone concentration of the cell due north of the ant)*
    
    """
    def __init__(self, starting_x, starting_y, turning_kernel, min_phi, delta_phi, sauturation_concentration):
        self.turning_kernel = turning_kernel
        self.min_phi = min_phi
        self.delta_phi = delta_phi
        self.sauturation_concentration = sauturation_concentration
        # self.last_x = starting_x
        # self.last_y = starting_y
        self.x = starting_x
        self.y = starting_y

        self.possible_moves = [(0, 1), (1, 1), (1,0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.direction = random.randint(1,7)
        self.is_lost =  True
        self.adjacent_cells_values = []


    def is_in_grid(self, grid, x = None, y = None):
        """
        Returns true if the posotion is in the grid and false if else
            Parameters:
                grid (df) : the dataframe to check
                x (int) : x position
                y (int) : y position

            Returns:
                (boolean)

        *Note:If x and y are not given they are assumed to be that of the ant's positons*
        """
        if x == None:
            x = self.x
        if y == None:
            y = self.y
        return  (x < grid.shape[0] and y < grid.shape[1] and x >= 0 and y >= 0)


    def find_adjacnet_cells_values(self, grid):
        """
        Finds the values of the cells adjacent to the ant

            Parameters:
                grid (df) : the dataframe to check
            Returns
                values (lst of floats) : the values of the adjecent cells

        """
        values = []
        for i, move in enumerate(self.possible_moves):
            x = self.x + move[0]
            y = self.y + move[1]

            ant_is_facing = (abs(i - self.direction) <= 1)
            is_in_grid = self.is_in_grid(grid, x, y)

            if (ant_is_facing and is_in_grid):
                values.append(grid[x][y])
            else: 
                values.append(0.0)
        return values

    def move(self):
        """
        Updates an ant's position forward in whichever direction it is facing
        """
        # self.last_x = self.x
        # self.last_y = self.y
        self.x += self.possible_moves[self.direction][0]
        self.y += self.possible_moves[self.direction][1]

    def explore(self):
        """
        Updates an exploring ant's direction
        """
        prob_go_straight = 1 - 2 * sum(self.turning_kernel)
        turning_kernel = [prob_go_straight] + self.turning_kernel
        turning_amount_choices = [0,1,2,3,4]
        turn_amount = random.choices(turning_amount_choices, weights=turning_kernel, k=1)[0]
        turn_direction = random.randint(-1, 1) #left or right
        new_direction = (self.direction + turn_amount * turn_direction + 8) % 8

        self.direction = new_direction

    def follow(self):
        """
        Updates an trail following ant's position and direction
        """
        trails_possible_moves = [i for i, e in enumerate(self.adjacent_cells_values) if e != 0.0]
        if len(trails_possible_moves) == 1:
            trail_direction  = trails_possible_moves[0]
            self.direction = trail_direction
        else: 
            self.fork(trails_possible_moves)

    def fork(self, trails_possible_moves):
        """
        Handles case of more than one trail near the ant
            Parameters:
                trails_possible_moves (lst of ints) : a list of directions in which a trail lies. 
        """
        strongest_trails_possible_moves = [i for i, e in enumerate(self.adjacent_cells_values) if e == max(self.adjacent_cells_values)]

        if self.direction in trails_possible_moves:
            pass

        elif (len(strongest_trails_possible_moves) > 1):
            self.is_lost = True
            self.explore()

        else: 
            self.direction = strongest_trails_possible_moves[0]

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

        #Ensures the concentration input is not greater than the saturation concentration
        concentration = max(trail_concentration, self.sauturation_concentration) 
        probability = (self.min_phi + self.delta_phi * concentration)/ 256
        return random.random() < probability


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
        sauturation_concentration = 0):

        self.ants = set()
        self.grid = pd.DataFrame(np.zeros((size, size))) 

        self.evaporation_rate = 1 
        self.tau = tau

        self.min_phi = min_phi
        self.delta_phi = delta_phi
        self.sauturation_concentration = sauturation_concentration
        self.turning_kernel = turning_kernel


    def draw(self):
        """
        Draws the Grid
        """
        ant_xs = []
        ant_ys = []
        center_x, center_y = self.grid.shape[0] // 2, self.grid.shape[1] // 2
        draw_grid = self.grid.copy()
        draw_grid[center_x][center_y] = 0
        for ant in self.ants:
            ant_xs.append((ant.x + .5))
            ant_ys.append((ant.y + .5))
        plt.pcolormesh(draw_grid, cmap='Greys')
        # plt.scatter(ant_xs, ant_ys) #this line is still in development
        plt.show()


    def deposit(self):
        """
        adds a set amount(tau) of pheramones to the cell where the ant is present
            Parameters:
                ant (Ant) : the ant which is depositing the pheramones
        """
        for ant in self.ants.copy():
            if (ant.is_in_grid(self.grid)):
                x = ant.x
                y = ant.y
                self.grid[x][y] += self.tau
            else:
                self.ants.remove(ant)

    def evaporate(self): 
        """
        Subtracts a set amount of pheramones from all cells in grid
        """
        self.grid.where(self.grid == 0, self.grid - self.evaporation_rate)


    def update_ants(self):
        """
        Updates an all ants positions and possible_moves
        """

        for ant in self.ants:
            ant.adjacent_cells_values = ant.find_adjacnet_cells_values(self.grid)

            if ant.near_trail():
                ant.is_lost = not ant.follows_trail()

            if ant.is_lost:
                ant.explore()
            else:
                ant.follow()
            ant.move()

        num_followers = 0
        num_lost = 0
        for ant in self.ants:
            if ant.is_lost:
                num_lost += 1
            else:
                num_followers += 1

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
        self.deposit()
        self.evaporate()
        F, L = self.update_ants()
        print("F = " + str(F))
        print("L = " + str(L))

    def save(self):
        """
        Saves the data in the model to csv's
        """
        self.grid.to_csv("grid.csv")
        ant_xs = []
        ant_ys = []
        for ant in self.ants:
            ant_xs.append((ant.x + .5))
            ant_ys.append((ant.y + .5))
        ant_positions = pd.DataFrame({'x':ant_xs, 'y':ant_xs})
        ant_positions.to_csv("ant_positions.csv")

size = 256
tau = 8
min_phi = 247
turning_kernel = [.36, .047, .008, .004]
model = Model(size, tau, min_phi, turning_kernel)

for i in range(1500):
    print(i)
    model.step()
model.draw()
model.save()