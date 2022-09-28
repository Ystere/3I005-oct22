import numpy as np
import matplotlib.pyplot as plt

# creer dictionnaire (?)
class Grid ():
	def __init__(self, att):
		self.att = att
		# Grille
		mat = np.zeros((10,10), dtype=int)
		size = len(mat)

		# Dictionnaire des correspondances bateau-taille
		dict_bat_size = { 1:5, 2:4, 3:3, 4:3, 5:2 }

		# Dictionnaire des correspondances identifiant-bateau
		dict_id_bat = { 1:"Porte-Avions", 2:"Croiseur", 3:"Contre-Torpilleur", 4:"Sous-Marin", 5:"Torpilleur" }

	def peut_placer(self, grid: Grid, bat: int, pos: tuple(int,int), dir: int):
		""" Grille * int * tuple(int, int) * int --> Bool

			Renvoie sous forme de booléen si le bateau b peut etre placé a la postion et avec la direction indiquées
		"""	
		# Placement du bateau
		lig_pos = pos[0]
		col_pos = pos[1]

		# Vérification du possible positionnement du bateau dans la grille
		size_bat = dict_bat_size.get(bat)
		if lig_pos + size_bat >= grid.size or col_pos + size_bat >= grid.size:
			print("Le bateau dépasse de la grille et n'est pas positionnable.")
			return False

		# dir = 1 --> vertical
		if dir: 
			for lig_v in range(lig_pos, lig_pos+bat):
				if grid[lig_v][col_pos] != 0:
					print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(dict_id_bat.get(bat), lig_v, col_pos))
					return False 

		# dir = 0 --> horizontal
		else:
			for col_v in range(col_pos, col_pos+bat):	
				if grid[lig_pos][col_v] != 0:
					print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(dict_id_bat(bat), lig_pos, col_v))
					return False 

	def place(self, grid: Grid, bat: int, pos: tuple(int, int), dir: int):
		""" Grille * int * tuple(int, int) * int --> Grille

			Renvoie la grille modifiée après un placement d'un bateau spécifié
		"""
		if not self.peut_placer(grid, bat, pos, dir):
			return grid
		else:
			if dir:
				for lig in range():
					grid[lig][col] = bat
					return grid
			else:
				for col in range():
					grid[lig][col] = bat
					return grid

	def place_alea(self, grille: Grid, bat: int):
		""" Grille * int --> Grille

			Renvoie la grille modifiée après un placement aléatoire d'un bateau spécifié
		"""
		coord = int(np.fix(self.size*np.random.random() + 1))

		rand_dir 	= 0 if np.random.random() <= 0.5 else 1 		# 50% de chance pour 0 ou 1
		rand_pos 	= (coord, coord)  								# cast vers int de (taille de la matrice+1)
		cond 		= peut_placer(grille, bat, rand_pos, rand_dir)
		while not cond:
			coord = int(np.fix(self.size*np.random.random() + 1))
			rand_dir 	= 0 if np.random.random() <= 0.5 else 1 
			rand_pos 	= (coord, coord)
			cond 		= peut_placer(grille, bat, rand_pos, rand_dir)
		return place(grille, bat, rand_pos, rand_dir)

	def display(self, grille: Grid):
		""" Grille --> None

			Affiche la grille de jeu.
		""" 
		plt.matshow(grid)
		plt.show()

	def eq(self, gridA, gridB):
		return
	

def create_grid():

	# Création d'une partie (?)
	return