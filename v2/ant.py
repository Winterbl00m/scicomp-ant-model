class Ant():
    def __init__(nest_location):
        self.x = nest_location
        self.y = nest_location
        self.direction = random.randint(1,7)
        self.food_seen = 0
        self.nest_location = nest_location

    def follow(self, nearby_pheromones):
        """
        Determines which trail a following ant will follow and updates its direction
            Parameters:
                nearby_pheromones (lst): the pheromone amount in the three cells in front of the ant
        """
        left, straight, right = nearby_pheromones

        #If trail ahead go stright
        if straight != 0.0:
            pass
        #Otherwise follow strongest trail
        elif left > right :
            self.direction = (self.direction + 1) % 8  
        elif right > left :
            self.direction = (self.direction - 1) % 8 

    def explore(self, turning_kernel):
        """
        Updates an exploring ant's direction
            Parameters:
                turning_kernel (lst) : a list of probabilities that an ant will turn
        """
        prob_go_straight = 1 - 2 * sum(turning_kernel)
        turning_probabilities = [prob_go_straight] + turning_kernel
        turning_amount_choices = [0,1,2,3,4]
        turn_amount = random.choices(turning_amount_choices, weights=turning_probabilities, k=1)[0]
        turn_direction = random.randint(-1, 1) #left or right

        new_direction = (self.direction + turn_amount * turn_direction + 8) % 8
        self.direction  = new_direction

    def gather(self, nearby_food, food, possible_moves):
        """
        Decrease food in field and send a gathering ant home 
            Parameters:
                ant (lst) : the ant to update
                nearby_food (lst): the food amount in the three cells in front of the ant
        """
        #Calculates where max nearby food is
        max_food_index = nearby_food.index(max(nearby_food)) - 1
        food_direction = (self.direction + max_food_index) % 8 
        food_x = self.x + possible_moves[food_direction][0]
        food_y = self.y + possible_moves[food_direction][1]

        #sets ant to return to the nest
        self.food_seen = food[food_x][food_y]
        #removes 1 food from location
        food[food_x][food_y] -= 1

    def go_to_nest(self, possible_moves):
        """
        Updates a ants direction to point towards nest
            Parameters:
                ant (lst) : the ant to update
        """
        x_direction_of_nest = np.sign(self.nest_location - self.x)
        y_direction_of_nest = np.sign(self.nest_location - self.y)
        self.direction = possible_moves.index((x_direction_of_nest, y_direction_of_nest))

    def ant_at_nest(self):
        """
        Updates and retuning ant's status if it is at the nest
        """
        at_nest = (self.x == self.nest_location and self.y == self.nest_location)
        if self.food_seen and at_nest:
            # sets a retuning ant at nest food_seen to 0
            self.food_seen = 0

