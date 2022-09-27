import numpy as np

# creer dictionnaire (?)
class Grid ():
	def __init__(self, att):
		self.att = att
		# Grille
		mat = np.zeros((10,10), dtype=int)
		size = len(mat)

	def peut_placer(self, grid: Grid, bat: int, pos: tuple(int,int), dir: int):
		""" Grille * dict(str, int) * tuple(int, int) * int -> Bool

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

	def place(self, grid: Grid, bat, pos: tuple(int, int), dir: int):
		if not self.peut_placer(grid, bat, pos, dir):
			return grid
		else:
			if dir:
				for lig in range():
					grid[lig][col] = bat
			else:
				for col in range():
					grid[lig][col] = bat

	def place_alea(self, grille, bat):
		return

	def display(self, grid):
		return	

	def eq(self, gridA, gridB):
		return
	

def create_grid():

	# Dictionnaire des correspondances bateau-taille
	dict_bat_size = { 1:5, 2:4, 3:3, 4:3, 5:2 }

	# Dictionnaire des correspondances identifiant-bateau
	dict_id_bat = { 1:"Porte-Avions", 2:"Croiseur", 3:"Contre-Torpilleur", 4:"Sous-Marin", 5:"Torpilleur"}

	# Création d'une partie (?)
	return