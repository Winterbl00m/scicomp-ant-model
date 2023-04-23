import random
import numpy as np 

class Ant:
    def __init__(self, board_size, turning_kernel, min_phi, delta_phi, sauturation_concentration):
        self.x = board_size // 2 
        self.y = board_size // 2
        self.direction = random.randint(1,7)
        self.mode = "explore"
        self.adjacent_cells_pheromones= []
        self.adjacent_cells_food = []
        self.board_size = board_size
        self.turning_kernel = turning_kernel
        self.possible_moves = [(0, 1), (1, 1), (1,0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.min_phi = min_phi
        self.delta_phi = delta_phi
        self.sauturation_concentration = sauturation_concentration

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

    def explore(self):
        """
        Updates an exploring ant's direction
        """
        prob_go_straight = 1 - 2 * sum(self.turning_kernel)
        turning_probabilities = [prob_go_straight] + self.turning_kernel
        turning_amount_choices = [0,1,2,3,4]
        turn_amount = random.choices(turning_amount_choices, weights=turning_probabilities, k=1)[0]
        turn_direction = random.randint(-1, 1) #left or right
        new_direction = (self.direction + turn_amount * turn_direction + 8) % 8

        self.direction = new_direction

    def follow(self):
        """
        Updates an trail following ant's position and direction
        """

        straight = self.adjacent_cells_pheromones[1]
        left = self.adjacent_cells_pheromones[0]
        right = self.adjacent_cells_pheromones[2]

        #If trail ahead go stright
        if self.adjacent_cells_pheromones[1] != 0.0:
            pass
        elif left > right :
            self.direction = (self.direction + 1) % 8  
        elif right > left :
            self.direction = (self.direction - 1) % 8 
        else: 
            self.mode = "explore"
            self.explore()

    def gather(self):
        """
        Updates a food gather ant's potistion and direction 
        """
        if any(ele > 0.0 for ele in adjacent_cells_food):
            self.mode = "go_home"
            self.go_home()

    def go_home(self):
        """
        Updates a returning ant's potistion and direction 
        """
        position = [self.x, self.y]
        next_move = np.sign((position - (board_size // 2)))
        if next_move != [0,0]:
            self.direction = self.possible_moves.index(tuple(next_move))
        else:
            self.mode = "explore"
            self.explore()

    def move(self):
        """
        Updates an ant's position forward in whichever direction it is facing
        """
        # self.last_x = self.x
        # self.last_y = self.y
        self.x += self.possible_moves[self.direction][0]
        self.y += self.possible_moves[self.direction][1]

    def find_adjacnet_cells_values(self, dataframe):
        """
        Finds the values of the cells adjacent to the ant

            Parameters:
                dataframe (df) : the dataframe to check
            Returns
                values (lst of floats) : the values of the adjecent cells

        """
        values = []
        for i in range(self.direction - 1, self.direction + 2, 1):
            i = i % 8 
            x = self.x + self.possible_moves[i][0] 
            y = self.y + self.possible_moves[i][1]
            is_in_grid = self.is_in_grid(dataframe, x, y)
            if is_in_grid:
                values.append(dataframe[x][y])
            else: 
                values.append(0.0)
        return values


    def follows_trail(self):
        """
        Determines if ant explores or follows a trail at any one time step.

        Returns True if ant will follow the trail
        """

        trail_concentration = max(self.adjacent_cells_pheromones)
        if trail_concentration:
            #Ensures the concentration input is not greater than the saturation concentration
            concentration = min(trail_concentration, self.sauturation_concentration) 
            probability = (self.min_phi + self.delta_phi * concentration)/ 256
            return random.random() < probability
        else:
            return False

    def smells_food(self):
        return False