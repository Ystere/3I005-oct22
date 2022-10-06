import numpy as np
import matplotlib.pyplot as plt
import copy
import proj1_p2

class Battle():
	def __init__(self):
		self.hit_count = 0
		self.rand_grid = generate_grid()

	def play(self, position):
		if self.rand_grid[position[0]][position[1]] != 0:
			self.hit_count += 1
			print("Bateau touché")
			return True
		print("Cible ratée")
		return False

	def victory(self):
		return True if hit_count == 17 else False
	
	def reset(self):
		self.hit_count = 0
		self.rand_grid = generate_grid()
		print("Partie réinitalisée")
	

class RandomPlayer():
	pass

class HeuristicPlayer():
	pass

class SimpleP_Player():
	pass

class MCMethodPlayer():
	pass