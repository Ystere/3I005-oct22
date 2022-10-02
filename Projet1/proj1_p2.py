import numpy as np
import matplotlib.pyplot as plt
import copy

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

		size_bat = self.dict_bat_size.get(bat)
		# dir = 1 --> vertical
		if dir:
			# Vérification du possible positionnement du bateau dans la grille
			if lig_pos + size_bat > self.size:
				#print("Le bateau dépasse de la grille et n'est pas positionnable.")
				return False
			for lig_v in range(lig_pos, lig_pos+size_bat):
				if self.grid[lig_v][col_pos] != 0:
					#print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(self.dict_id_bat.get(bat), lig_v, col_pos))
					return False 

		# dir = 0 --> horizontal
		else:
			# Vérification du possible positionnement du bateau dans la grille
			if col_pos + size_bat > self.size:
				#print("Le bateau dépasse de la grille et n'est pas positionnable.")
				return False
			for col_v in range(col_pos, col_pos+size_bat):	
				if self.grid[lig_pos][col_v] != 0:
					#print("Bateau impossible a placer : un bateau de type {} est en '{},{}'".format(self.dict_id_bat.get(bat), lig_pos, col_v))
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
		x = int(np.fix(self.size*np.random.random()))
		y = int(np.fix(self.size*np.random.random()))

		rand_dir 	= 0 if np.random.random() <= 0.5 else 1 		# 50% de chance pour 0 ou 1
		rand_pos 	= (x, y)  								# cast vers int de (taille de la matrice+1)
		cond 		= self.peut_placer(bat, rand_pos, rand_dir)
		while not cond:
			x = int(np.fix(self.size*np.random.random()))
			y = int(np.fix(self.size*np.random.random()))
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
	return np.equal(gridA.grid, gridB.grid).all()
	

def generate_grid():
	grid = Grid()
	for i in range(1, 6):
		grid.place_alea(i)

	return grid

def calcul_nb_place(bat: int, grid: Grid):
	""" int * Grille --> int

		Renvoie le nombre de façons de placer un bateau donné sur une grille vide
	"""
	n = 0
	
	for posx in range(0, grid.size):	 # pour chaque position
		for posy in range(0, grid.size):
			for dir in [0,1]:			 # pour chaque direction
				if grid.peut_placer(bat, (posx, posy), dir): # test de placement
					n += 1
	return n

def calcul_nb_place_liste(list_bat:list, grid: Grid):
	""" List * Grille --> int

		Renvoie le nombre de façon de placer une liste de bateaux sur une grille vide
	"""
	l = len(list_bat)
	n = 0
	new_grid = Grid()
	new_grid.grid = copy.deepcopy(grid.grid)	# grille temp
	if l == 1:		# liste de un bateau
		return calcul_nb_place(list_bat[0], grid)
	if l == 2:		# liste de deux bateaux
		for posx in range(0, grid.size):							# pour chaque position dans la grille
			for posy in range(0, grid.size):
				for dir in [0,1]:									# pour chaque direction
					new_grid.place(list_bat[0], (posx, posy), dir)	# on place le dernier bateau dans la grille
					if not eq(grid, new_grid):						# on teste si le bateau a pu être placé
						n += calcul_nb_place(list_bat[1], new_grid)	# on calcule
					new_grid.grid = copy.deepcopy(grid.grid)		# on retire le bateau de la grille
		return n
	else:			# liste de plusieurs bateaux
		for posx in range(0, grid.size):							# pour chaque position dans la grille
			for posy in range(0, grid.size):
				for dir in [0,1]:									# pour chaque direction
					new_grid.place(list_bat[0], (posx, posy), dir)	# on place le bateau dans la grille
					if not eq(grid, new_grid):						# on teste si le bateau a pu être placé
						n += calcul_nb_place_liste(list_bat[1:], new_grid)	# on calcule
						new_grid.grid = copy.deepcopy(grid.grid)	# on retire le bateau de la grille
		return n

def nb_generation(grid: Grid):
	""" Grille --> int

		Renvoie le nombre de grilles générées aléatoirement 
		jusqu’à ce que la grille générée soit égale à la grille passée en paramètre 
	"""
	n = 0
	while not eq(grid, generate_grid()):
		n += 1
	return n

#	Test

grid1 = Grid()
nbp = calcul_nb_place(1, grid1)
print(nbp)
nbpl = calcul_nb_place_liste([1,2,3], grid1)
print(nbpl)
grid1 = generate_grid()
#nbg = nb_generation(grid1)
#print(nbg)

#grid1 = grid1.place(3, (1,1), 1)
#grid1 = grid1.place_alea(4)
#grid1.display()

#grid2 = generate_grid()
#grid2.display()
