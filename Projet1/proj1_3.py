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


	def distribution(self, player, n: int) -> tuple:
		""" On joue n fois une version de jeu, et on stocke dans un tableau le nombre 
 			le nombre de tours pour chaque victoire et dans un autre la frequence des nombres de tours
		"""
		hits = []
		freq = [0 for i in range(17, 101)]
		for i in range(n) :
			hits.append(player.play())
			freq[player.play() - 17] += 1
			player.__init__()
		return hits, freq

	def display_distribution(self, player, n: int) -> float:
		""" Calcule et affiche la distribution et l'espérance du nombre de victoire
			en fonction du nombre de coups d'une version de jeu joué 
		"""
		(hits, freq) = self.distribution(player, n)
		esp = 0
		for i in range(17, 101) :
			esp += i * freq[i - 17]
		esp = esp/n
		plt.hist(hits, bins = 100)
		plt.title("Distribution de la v.a pour {} tests Version {}".format(n, player.name))
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
print("Esperence Version aléatoire: {}".format(b.display_distribution(r, 1000)))
print("Nombre de coups 'Version aléatoire': {}".format(r.play()))
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
print("Esperence Version heuristique: {}".format(b.display_distribution(h, 1000)))

print("Nombre de coups 'Version heuristique': {}".format(h.play()))
#--------------------

class SimpleP_Player():
	def __init__(self):
		self.game = Battle()
		self.name = "probabiliste simplifiée"
		self.boat_left = list(map(list, g.Grid().dict_bat_size.items()))
		self.probas = g.generate_grid()
  
	def play(self) -> int: 
		""" Cette fonction va simuler un coup joué par un joueur probabiliste simplifié.
  
		En fonction d'un bateau, on calcule la probabilité qu'il soit présent sur la case (sans tenir compte des positions des autres bateaux)

		On somme la probabilité pour un bateau donné et on obtient la probabilité jointe - si on considère que la position des autres bateaux est indépendante par rapport a celui choisi.
  
		On obtient en retour le nombre de coups a jouer afin de gagner la partie.
		"""
		
		# self.probas : list(list(int)), est ré-initialisée à chaque tour
		self.probas = g.generate_grid()

		# t : int, décalage
		t = 0
		# bonus : int
		bonus = 0
		# peut_poser : boolean
		peut_poser = False

		effect = -1
		# effect est <= -1 quand la case visée a déjà été jouée
		while (effect <= -1) :
			""" Calculer la probabilité pour chaque case de contenir ce
			bateau sans tenir compte de la position des autres bateaux.
			"""
			# Pour chaque bateau restant :
			for b in self.boat_left :
				# Pour chaque case :
				for i in range(10) :
					for j in range(10) :
						# Si la case à été jouée et n'était pas un bateau :
						if self.game.play_grid.layout[i,j] and not self.game.rand_grid.layout[i,j]:
							# Pas de bateau ici
							self.probas[i][j] = 0
						else :
							t = 0
							bonus = 0
							# Si la case était un bateau et a été jouée
							if self.game.play_grid.layout[i,j] and self.game.rand_grid.layout[i,j]:
								# Les probabilités seront plus grandes
								bonus = 1
								self.probas[i][j] = 0
								t = 1

							""" position verticale """
							peut_poser = True
							# Parcours des cases direction sud :
							for u in range(1, b[0][1]) :
								# Si la case explorée est hors-limite ou
								# qu'elle a été jouée et n'a pas touché de
								# bateau :
								if not self.game.play_grid.check_bound((i+u,j)) or (self.game.play_grid.layout[i,j] and not self.game.rand_grid.layout[i,j]):
									peut_poser = False
									break
								# Si la case explorée est un bateau touché, les
								# chances qu'une autre case bateau se trouve
								# proche sont plus grandes :
								if self.game.play_grid.layout[i,j] and self.game.rand_grid.layout[i,j] :
									# On augmente les probabilités des cases explorées
									bonus += 1
							""" Attribution des probabilités """
							if peut_poser :
								# on peut attribuer leurs probabilités aux
								# cases que le bateau pourrait couvrir sur sa longueur (bonus *2)
								for u in range(t, b[0][1]) :
									if not (self.game.play_grid.layout[i+u,j] and self.game.rand_grid.layout[i,j]) :
										self.probas.layout[i+u,j] += 1 + bonus * 2

							"""position horizontale """
							peut_poser = True
							for v in range(1, b[0][1]) :
								# Si la case explorée est hors-limite ou
								# qu'elle a été jouée et n'a pas touché de
								# bateau :
								if not self.game.play_grid.check_bound((i,j+v)) or (self.game.play_grid.layout[i,j+v] and not self.game.rand_grid.layout[i,j+v]):
									peut_poser = False
									break
								# Si la case explorée est un bateau touché, les
								# chances qu'une autre case bateau se trouve
								# proche sont plus grandes
								if self.game.play_grid.layout[i,j+v] and self.game.rand_grid.layout[i,j+v] :
									bonus += 1
							""" Attribution des probabilités """
							if peut_poser :
								# on peut attribuer leurs probabilités aux
								# cases que le bateau pourrait couvrir sur sa longueur (bonus *2)
								for v in range(t, b[0][1]) :
									if not (self.game.play_grid.layout[i,j+v] and self.game.rand_grid.layout[i,j+v]) :
										self.probas.layout[i,j+v] += 1 + bonus * 2

			"""Choisir une position dans probas"""
			# C'est le moment où après avoir calculé une grille de
			# probabilités on choisit la case ayant la plus forte probabilité
			# de contenir un bateau
			maxiProba = np.argmax(self.probas.layout).all()
			x = maxiProba // 10
			y = maxiProba + 10 % 10
			effect = self.game.play((x, y))

		
		"""Màj des bateaux restants en cas de tir réussi"""
		if effect != 0 :
			for i in range(len(self.boat_left)) :
				if self.boat_left[i][0] == effect :
					self.boat_left[i] = (self.boat_left[i][0], self.boat_left[i][1] - 1)

		return effect

#--------------------
s = SimpleP_Player()

print("Esperence Version {}: {}".format(s.name, b.display_distribution(h, 1000)))
print("Nombre de coups 'Version {}': {}".format(s.name, s.play()))
#--------------------
