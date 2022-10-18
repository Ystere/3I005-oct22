import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import proj1_p2 as g
import time
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
		if not self.play_grid.check_bound(pos):
			return False
		(x, y) = pos
		if not self.play_grid.layout[x, y]:
			#print("Coup non joué ici auparavant.")
			self.attempt_count += 1
			self.play_grid.layout[x, y] = True
			if self.rand_grid.layout[x, y] != 0:
				#print("Bateau touché !")
				self.hit_count += 1
				return True
			else:
				#print("Manqué...")
				return False
		else:
			#print("Coup déja joué ici, tentez une autre position.")
			return False

	def victory(self) -> bool:
		return self.hit_count == 17

	def reset(self) -> None:
		self.hit_count = 0
		self.attempt_count = 0
		self.rand_grid = g.generate_grid()
		self.play_grid = g.Grid()
		print("Partie réinitalisée.")


	def distribution(self, player) :
		""" On joue 1000 fois une version de jeu, et on stocke dans un tableau le nombre 
 			le nombre de tours pour chaque victoire
		"""
		hits = []
		freq = [0 for i in range(17, 101)]
		for i in range(1000) :
			hits.append(player.play())
			freq[player.play() - 17] += 1
			player.__init__()
		return hits, freq

	def display_distribution(self, player):
		""" Calcule et affiche la distribution et l'espérance du nombre de victoire
			en fonction du nombre de coups d'une version de jeu joué 
		"""
		hits, freq = self.distribution(player)
		esp = 0
		for i in range(17, 101) :
			esp += i * freq[i - 17]
		esp = esp/1000
		arr = np.array(hits)
		plt.hist(hits, bins = 100)
		plt.title("Distribution de la v.a pour 1000 tests Version {}".format(player.name))
		plt.xlabel('Nombre de tours')
		plt.ylabel('Fréquence')
		plt.show()
		return esp


class RandomPlayer():
	# hypothèses
	# Jeu a un joueur : 17 cases "remplies" donc nombres minimal de coups a jouer = 17
	# Espérance = sum([17 <= k <= 100], k*P(X = k))*
	# A vérifier
	def __init__(self):
		self.game = Battle()
		self.name = "Random"

	def play(self) -> int:
		""" Renvoie le nombre de coups joués avant la victoire

		Cette fonction va tenter de jouer un coup valide tant que la condition de victoire n'est pas atteinte.
		Version aléatoire
		"""
		random_grid = self.game.rand_grid
		while not self.game.victory():
			x = rng.integers(random_grid.size)
			y = rng.integers(random_grid.size)
			self.game.play((x, y))
		return self.game.attempt_count

# -----Test----
b = Battle()
r = RandomPlayer()
print("Esperence Version aléatoire: {}".format(b.display_distribution(r)))
print("Nombre de coups 'Version aléatoire': {}".format(r.play()))
s = 0
for k in range(17, 101):
	s = s + k*(math.comb(83, k-17)/math.comb(100, k))
print(s)

# -------------


class HeuristicPlayer():
	def __init__(self):
		self.game = Battle()
		self.name = "Heuristique"

	def play(self) -> int:
		""" Renvoie le nombre de coups joués avant la victoire

		Version heuristique
		"""
		random_grid = self.game.rand_grid
		prev_hit = 0
		while not self.game.victory():
			if self.game.hit_count != prev_hit:  # si on a touché un bateau
				for k, xc, yc in [("left", x, y-1), ("right", x, y+1), ("down", x-1, y), ("up", x+1, y)]:
					prev_hit = self.game.hit_count
					self.game.play((xc, yc))
					cpt = 0
					while self.game.hit_count != prev_hit:  # si touché dans une case connexe on continue sur le meme chemin
						cpt += 1
						prev_hit = self.game.hit_count
						if k == "left":
							self.game.play((xc, yc-cpt))
						if k == "right":
							self.game.play((xc, yc+cpt))
						if k == "down":
							self.game.play((xc-cpt, yc))
						if k == "up":
							self.game.play((xc+cpt, yc))
			else:
				x = rng.integers(random_grid.size)
				y = rng.integers(random_grid.size)
				prev_hit = self.game.hit_count
				self.game.play((x, y))

		return self.game.attempt_count

#--------------------
h = HeuristicPlayer()
print("Esperence Version heuristique: {}".format(b.display_distribution(h)))

print("Nombre de coups 'Version heuristique': {}".format(h.play()))
#--------------------

class SimpleP_Player():
	def __init__(self):
		self.game = Battle()
		self.name = "probabiliste simplifiée"

	def play(self) -> int: 
		""" Cette fonction va simuler un coup joué par un joueur probabiliste simplifié.
  
		En fonction d'un bateau, on calcule la probabilité qu'il soit présent sur la case (sans tenir compte des positions des autres bateaux)

		On somme la probabilité pour un bateau donné et on obtient la probabilité jointe - si on considère que la position des autres bateaux est indépendante par rapport a celui choisi.
  
		On obtient en retour le nombre de coups a jouer afin de gagner la partie.
		"""
		

		return
	
class MCMethodPlayer():
	pass
