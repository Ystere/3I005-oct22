import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import proj1_p2 as g
from numpy.random import default_rng
rng = default_rng()

class Battle():
	def __init__(self):
		self.hit_count 		= 0
		self.attempt_count 	= 0
		self.rand_grid 		= g.generate_grid()
		self.play_grid		= g.Grid()


	def play(self, position: tuple) -> bool:
		""" Retourne si le coup joué est touché ou non.

			Hypothèse : Le coup n'a pas déja été joué ici.
		"""
		if not self.play_grid.layout[position[0],position[1]]:
			print("Coup non joué ici auparavant.")
			self.attempt_count += 1
			self.play_grid.layout[position[0],position[1]] = True
			if self.rand_grid.layout[position[0],position[1]] != 0:
				print("Bateau touché !")
				self.hit_count += 1
				return True
			else: 
				print("Manqué...")
				return False
		else:
			print("Coup déja joué ici, tentez une autre position.")
			return False

	def victory(self) -> bool:
		return self.hit_count == 17

	def reset(self) -> None:
		self.hit_count = 0
		self.rand_grid = g.generate_grid()
		print("Partie réinitalisée.")
	

class RandomPlayer():
	# hypothèses 
	# Jeu a un joueur : 17 cases "remplies" donc nombres minimal de coups a jouer = 17
	# Espérance = sum([17 <= k <= 100], k*P(X = k))*
	# A vérifier
	def __init__(self):
		self.battle = Battle()

	def random_play(self) -> int:
		""" Renvoie le nombre de coups joués avant la victoire

		Cette fonction va tenter de jouer un coup valide tant que la condition de victoire n'est pas atteinte.
		"""
		random_grid = self.battle.rand_grid
		while not self.battle.victory():	
			x = rng.integers(random_grid.size)
			y = rng.integers(random_grid.size)
			self.battle.play((x,y))		
		return self.battle.attempt_count


#-----Test----
r = RandomPlayer()

n = r.random_play()
print(n)
s=0
for k in range(17, 101):
    s = s + k*(math.comb(83, k-17)/math.comb(100, k))
print(s)
#-------------

class HeuristicPlayer():
	pass

class SimpleP_Player():
	pass

class MCMethodPlayer():
	pass
