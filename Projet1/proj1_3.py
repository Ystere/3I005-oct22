import numpy as np
import matplotlib.pyplot as plt
import copy
import proj1_p2

class Battle():
	def __init__(self):
		self.hit_count 		= 0
		self.attempt_count 	= 0
		self.rand_grid 		= generate_grid()
		self.play_grid 		= np.zeros((10, 10), dtype=bool)


	def play(self, position):
		# Vérification de la présence d'un marqueur dans la grille de coups joués

		# Si le marqueur est présent, ne rien faire
		# Sinon, vérifier l'identifiant dans la grille de jeu. Si différent de 0, coup touché

		""" tuple(int, int) --> bool

			Retourne si le coup joué est touché ou non.
		"""
		self.attempt_count += 1
		if not self.play_grid[position[0]][position[1]]:
			print("Coup non joué ici auparavant.")
			if self.rand_grid[position[0]][position[1]] != 0:
				print("Bateau touché !")
				self.hit_count += 1
				return True
			else: 
				print("Manqué...")
				return False
		else:
			print("Coup déja joué ici, tentez une autre position.")
			return False

	def victory(self):
		return hit_count == 17
	def reset(self):
		self.hit_count = 0
		self.rand_grid = generate_grid()
		print("Partie réinitalisée")
	

class RandomPlayer():
	# hypothèses 
	# Jeu a un joueur : 17 cases "remplies" donc nombres minimal de coups a jouer = 17
	# Espérance = sum([17 <= k <= 100], k*P(X = k))*
	# A vérifier

	pass

class HeuristicPlayer():
	pass

class SimpleP_Player():
	pass

class MCMethodPlayer():
	pass