import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import proj1_p2 as g
from numpy.random import default_rng
rng = default_rng()


class Battle():
	def __init__(self):
		self.hit_count = 0
		self.attempt_count = 0
		self.rand_grid = g.generate_grid()
		self.play_grid = g.Grid()

	def play(self, pos: tuple) -> bool:
		""" Retourne si le coup joué est touché ou non.

				Hypothèse : Le coup n'a pas déja été joué ici.
		"""
		print(pos)
		if pos[0] in range(0, self.play_grid.size) and pos[1] in range(0, self.play_grid.size):
			if not self.play_grid.layout[pos[0], pos[1]]:
				print("Coup non joué ici auparavant.")
				self.attempt_count += 1
				self.play_grid.layout[pos[0], pos[1]] = True
				if self.rand_grid.layout[pos[0], pos[1]] != 0:
					print("Bateau touché !")
					self.hit_count += 1
					return True
				else:
					print("Manqué...")
					return False
			else:
				print("Coup déja joué ici, tentez une autre position.")
				return False
		else:
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
		Version aléatoire
		"""
		random_grid = self.battle.rand_grid
		while not self.battle.victory():
			x = rng.integers(random_grid.size)
			y = rng.integers(random_grid.size)
			self.battle.play((x, y))
		return self.battle.attempt_count


# -----Test----
r = RandomPlayer()

#print(r.random_play())
s = 0
for k in range(17, 101):
	s = s + k*(math.comb(83, k-17)/math.comb(100, k))
print(s)
# -------------


class HeuristicPlayer():
	def __init__(self):
		self.battle = Battle()

	def hplay(self) -> int:
		""" Renvoie le nombre de coups joués avant la victoire

		Version heuristique
		"""
		random_grid = self.battle.rand_grid
		prev_hit = 0
		while not self.battle.victory():
			if self.battle.hit_count != prev_hit:  # si on a touché un bateau
				for k, xc, yc in [("left", x, y-1), ("right", x, y+1), ("down", x-1, y), ("up", x+1, y)]:
					prev_hit = self.battle.hit_count
					self.battle.play((xc, yc))
					cpt = 0
					while self.battle.hit_count != prev_hit:  # si touché dans une case connexe on continue sur le meme chemin
						cpt += 1
						prev_hit = self.battle.hit_count
						if k == "left":
							self.battle.play((xc, yc-cpt))
						if k == "right":
							self.battle.play((xc, yc+cpt))
						if k == "down":
							self.battle.play((xc-cpt, yc))
						if k == "up":
							self.battle.play((xc+cpt, yc))
			else:
				x = rng.integers(random_grid.size)
				y = rng.integers(random_grid.size)
				prev_hit = self.battle.hit_count
				self.battle.play((x, y))

		return self.battle.attempt_count


h = HeuristicPlayer()
print(h.hplay())


class SimpleP_Player():
	pass


class MCMethodPlayer():
	pass
