import numpy as np
import matplotlib.pyplot as plt

class Grid ():
	def __init__(self):
		# Grille
		self.grid = np.zeros((10,10), dtype=int)
		self.size = len(self.grid)

		# Dictionnaire des correspondances bateau-taille
		self.dict_bat_size = { 1:5, 2:4, 3:3, 4:3, 5:2 }

		# Dictionnaire des correspondances identifiant-bateau
		self.dict_id_bat = { 1:"Porte-Avions", 2:"Croiseur", 3:"Contre-Torpilleur", 4:"Sous-Marin", 5:"Torpilleur" }

	def peut_placer(self, bat: int, pos: tuple, dir: int):
		""" Grille * int * tuple(int, int) * int --> Bool

			Renvoie sous forme de booléen si le bateau b peut etre placé a la postion et avec la direction indiquées
		"""	
		# Placement du bateau
		lig_pos = pos[0]
		col_pos = pos[1]

		# Vérification du possible positionnement du bateau dans la grille
		size_bat = self.dict_bat_size.get(bat)
		if lig_pos + size_bat >= self.size or col_pos + size_bat >= self.size:
			print("Le bateau dépasse de la grille et n'est pas positionnable.")
			return False

		# dir = 1 --> vertical
		if dir: 
			for lig_v in range(lig_pos, lig_pos+size_bat):
				if self.grid[lig_v][col_pos] != 0:
					print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(self.dict_id_bat.get(bat), lig_v, col_pos))
					return False 

		# dir = 0 --> horizontal
		else:
			for col_v in range(col_pos, col_pos+size_bat):	
				if self.grid[lig_pos][col_v] != 0:
					print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(self.dict_id_bat.get(bat), lig_pos, col_v))
					return False 
		return True

	def place(self, bat: int, pos: tuple, dir: int):
		""" Grille * int * tuple(int, int) * int --> Grille

			Renvoie la grille modifiée après un placement d'un bateau spécifié
		"""

		# Placement du bateau
		lig_pos = pos[0]
		col_pos = pos[1]

		# Taille du bateau
		size_bat = self.dict_bat_size.get(bat)

		# Placement du bateau
		if not self.peut_placer(bat, pos, dir):
			return self
		else:
			# dir = 1 --> vertical
			if dir:
				for lig_v in range(lig_pos, lig_pos+size_bat):
					self.grid[lig_v][col_pos] = bat
			# dir = 0 --> horizontal
			else:
				for col_v in range(col_pos, col_pos+size_bat):
					self.grid[lig_pos][col_v] = bat
			
		return self

	def place_alea(self, bat: int):
		""" Grille * int --> Grille

			Renvoie la grille modifiée après un placement aléatoire d'un bateau spécifié
		"""
		x = int(np.fix(self.size*np.random.random() + 1))
		y = int(np.fix(self.size*np.random.random() + 1))

		rand_dir 	= 0 if np.random.random() <= 0.5 else 1 		# 50% de chance pour 0 ou 1
		rand_pos 	= (x, y)  								# cast vers int de (taille de la matrice+1)
		cond 		= self.peut_placer(bat, rand_pos, rand_dir)
		while not cond:
			x = int(np.fix(self.size*np.random.random() + 1))
			y = int(np.fix(self.size*np.random.random() + 1))
			rand_dir 	= 0 if np.random.random() <= 0.5 else 1 
			rand_pos 	= (x, y)
			cond 		= self.peut_placer(bat, rand_pos, rand_dir)
		self.place(bat, rand_pos, rand_dir)
		return self

	def display(self):
		""" Grille --> None

			Affiche la grille de jeu.
		""" 
		plt.matshow(self.grid)
		plt.show()

def eq(gridA, gridB):
	""" Grille * Grille --> Bool

		Renvoie la valeur booléenne d'égalité entre deux grilles de jeu.
	"""
	return np.equals(gridA.grid, gridB.grid)
	

def generate_grid():
	grid = Grid()
	for i in range(1, 5):
		grid.place_alea(i)

	return grid

def calcul_nb_place(bat: int, grid: Grid):
    """ int * Grille --> int

        Renvoie le nombre de façons de placer un bateau donné sur une grille vide
    """
    size_grid = grid.size
    n = 0
    for dir in range(0, 2):
        for posx in range(0, size_grid):
            for posy in range(0, size_grid):
                if grid.peut_placer(bat, (posx, posy), dir):
                    n += 1
    return n




#	Test

grid1 = Grid()
nb = calcul_nb_place(5, grid1)
print(nb)

#grid1 = grid1.place(3, (1,1), 1)
#grid1 = grid1.place_alea(4)
#grid1.display()

#grid2 = generate_grid()
#grid2.display()
