import numpy as np
from numpy.random import default_rng
rng = default_rng()

import numpy.matlib as npm
import matplotlib.pyplot as plt
import copy

def fix(value: float) -> int:
	""" Retourne l'entier le plus proche de la valeur passée en argument.
	"""
	return np.fix(value)

def copy(O):
	return copy.deepcopy(O)

class Grid ():
	def __init__(self):
		# Grille
		self.layout = npm.zeros((10,10), dtype=int)
		self.size = len(self.layout)

		# Dictionnaire des correspondances bateau-taille
		self.dict_bat_size = { 1:5, 2:4, 3:3, 4:3, 5:2 }

		# Dictionnaire des correspondances identifiant-bateau
		self.dict_id_bat = { 1:"Porte-Avions", 2:"Croiseur", 3:"Contre-Torpilleur", 4:"Sous-Marin", 5:"Torpilleur" }

	def get_size(self, bat: int) -> int:
		""" Renvoie la taille d'un bateau donné par son identifiant
		"""
		return self.dict_bat_size.get(bat)

	def peut_placer(self, bat: int, pos: tuple, dir: int) -> bool:
		""" Retourne sous forme de booléen si le bateau b peut etre placé a la postion et avec la direction indiquées
		"""	
		# Placement du bateau
		lig_pos = pos[0]
		col_pos = pos[1]

		size_bat = self.get_size(bat)
		# dir = 1 --> vertical
		if dir:
			# Vérification du possible positionnement du bateau dans la grille
			if lig_pos + size_bat > self.size:
				#print("Le bateau dépasse de la grille et n'est pas positionnable.")
				return False
			for lig_v in range(lig_pos, lig_pos+size_bat):
				if self.layout[lig_v,col_pos] != 0:
					#print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(self.dict_id_bat.get(bat), lig_v, col_pos))
					return False 

		# dir = 0 --> horizontal
		else:
			# Vérification du possible positionnement du bateau dans la grille
			if col_pos + size_bat > self.size:
				#print("Le bateau dépasse de la grille et n'est pas positionnable.")
				return False
			for col_v in range(col_pos, col_pos+size_bat):	
				if self.layout[lig_pos,col_v] != 0:
					#print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(self.dict_id_bat.get(bat), lig_pos, col_v))
					return False 
		return True

	def place(self, bat: int, pos: tuple, dir: int) -> list:
		""" Retourne la disposition de la grille modifiée après un placement d'un bateau spécifié
		"""

		# Placement du bateau
		lig_pos = pos[0]
		col_pos = pos[1]

		# Taille du bateau
		size_bat = self.get_size(bat)

		# Placement du bateau
		if not self.peut_placer(bat, pos, dir):
			return self
		else:
			# dir = 1 --> vertical
			if dir:
				for lig_v in range(lig_pos, lig_pos+size_bat):
					self.layout[lig_v,col_pos] = bat
			# dir = 0 --> horizontal
			else:
				for col_v in range(col_pos, col_pos+size_bat):
					self.layout[lig_pos,col_v] = bat
			return self

	def process_place_alea(self) -> tuple:
		""" Processus condensé aidant la fonction `place_alea`.
		"""
		x = rng.integers(2)		# Générateur pseudo-aléatoire d'entiers
		y = rng.integers(2)

		drand 	= 0 if rng.random() <= 0.5 else 1
		prand 	= (x, y)  										
		return (drand, prand)

	def place_alea(self, bat: int) -> list:
		""" Retourne la dispoition de la grille modifiée après un placement aléatoire d'un bateau spécifié
		"""
		(drand, prand) 	= self.process_place_alea()
		truth 			= self.peut_placer(bat, prand, drand)
		while not truth:
			(drand, prand)	= self.process_place_alea()
			truth 			= self.peut_placer(bat, prand, drand)
		self.place(bat, prand, drand)
		return self.layout

	def display(self, grid) -> None:
		""" Affiche la grille de jeu.
		""" 
		plt.matshow(self.layout)
		plt.show()

def eq(gridA: Grid, gridB: Grid) -> bool:
	""" Retourne la valeur booléenne d'égalité entre deux grilles de jeu.
	"""
	return np.equal(gridA.layout, gridB.layout).all()
	

def generate_grid() -> Grid:
	""" Retourne une grille générée aléatoirement.
	"""
	result = Grid()
	for i in range(1, 6):
		result.place_alea(i)
	return result

def calcul_nb_place(bat: int, grid: Grid) -> int:
	""" Renvoie le nombre de façons de placer un bateau donné sur une grille vide.
	"""
	count = 0
	for posx in range(0, grid.size):	 						# pour chaque position
		for posy in range(0, grid.size):
			for dir in [0,1]:			 						# pour chaque direction
				positer = (posx, posy)
				if grid.peut_placer(bat, positer, dir): 	# test de placement
					count += 1
	return count

def calcul_nb_place_liste(list_bat: list, grid: Grid) -> int:
	""" Renvoie le nombre de façon de placer une liste de bateaux sur une grille vide.
	"""
	items = len(list_bat)
	count = 0
	tempgrid = Grid()
	tempgrid.layout = copy(grid.layout)				# grille temp
	if items == 1:													# liste de un bateau
		return calcul_nb_place(list_bat[0], grid)
	if items == 2:													# liste de deux bateaux
		for posx in range(0, grid.size):							# pour chaque position dans la grille
			for posy in range(0, grid.size):
				for dir in [0,1]:									# pour chaque direction
					tempgrid.place(list_bat[0], (posx, posy), dir)	# on place le dernier bateau dans la grille
					if not eq(grid, tempgrid):						# on teste si le bateau a pu être placé
						count += calcul_nb_place(list_bat[1], tempgrid)	# on calcule
					tempgrid.layout = copy.deepcopy(grid.layout)		# on retire le bateau de la grille
		return count
	else:														# liste de plusieurs bateaux
		for posx in range(0, grid.size):							# pour chaque position dans la grille
			for posy in range(0, grid.size):
				for dir in [0,1]:									# pour chaque direction
					tempgrid.place(list_bat[0], (posx, posy), dir)	# on place le bateau dans la grille
					if not eq(grid, tempgrid):						# on teste si le bateau a pu être placé
						count += calcul_nb_place_liste(list_bat[1:], tempgrid)	# on calcule
						tempgrid.layout = copy.deepcopy(grid.layout)	# on retire le bateau de la grille
		return count

def nb_generation(grid: Grid) -> int:
	""" Renvoie le nombre de grilles générées aléatoirement, jusqu'à ce que la grille générée soit égale à la grille passée en paramètre 
	"""
	count = 0
	while not eq(grid, generate_grid()):
		count += 1
	return count

######==========	Jeux de tests	==========######

grid1 = generate_grid()
print(grid1.layout)

#grid2 = Grid()
#print(grid2.layout)
#nbp = calcul_nb_place(1, grid1)
#print(nbp)
#nbpl = calcul_nb_place_liste([1,2,3], grid1)
#print(nbpl)
#grid1 = generate_grid()
#nbg = nb_generation(grid1)
#print(nbg)

#grid1 = grid1.place(3, (1,1), 1)
#grid1 = grid1.place_alea(4)

#grid1.display()

#grid2 = generate_grid()
#grid2.display()
