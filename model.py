import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Ant:
	def __init__(self, grid):
		self.last_position: (x,y) where x and y are ints
		self.position: (x,y) where x and y are ints
		self.direction: (Δx, Δy) where Δx or Δy can be -1, 0, 1
		self.is_lost: boolean
		self.min_phi: minimum value of fidelity
		self.delta_phi: 0
		self.sauration_concentration : pheromone level at which antennae saturate

	def explore(self):
        """
        Updates an exploring ant's position and direction
        """
        pass

    def follow(self):
    	"""
    	Updates an trail following ant's position and direction
    	"""
    	pass

    def turn_explore(self):
    	"""
		Updates an exploring ant's direction
    	"""
    	pass


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
		self.ants = {}
		self.grid = pd.DataFrame(np.zeros((256, 256)))
		self.evaporation_rate = 0 
		self.tau = 0 

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
			x = ant.position[0]
			y = ant.position[1]
			self.grid[x][y] += tau

	def evaporate(self): 
		"""
		Subtracts a set amount of pheramones from all cells in grid
		"""
		pass 

	def update_ants(self):
		"""
    	Updates an all ants positions and directions
    	"""
    	pass


	def step(self):
		"""
		Simulates one time step
		""" 
		self.evaporate()
		self.update_ants()
		self.deposit()		
		self.draw()