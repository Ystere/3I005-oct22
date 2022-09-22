import numpy as np

class Grid ():
	def __init__(self, att):
		self.att = att

	def peut_placer(self, grid, bat, pos, dir):
		# creer dictionnaire (?)

		lig_pos = pos[0]
		col_pos = pos[1]
		# dir = 1 --> vertical
		if dir: 
			for lig_v in range(lig_pos, lig_pos+bat):
				if grid[lig_v][col_pos] != 0:
					print("Bateau impossible a placer : un bateau de type {} est en {}".format(bat, ))
					return False 
		# dir = 0 --> horizontal
		else:
			for col_v in range(col_pos, col_pos+bat):	
				if grid[lig_pos][col_v] != 0:
					print("Bateau impossible a placer : un bateau de type {} est en {}".format(bat, ))
					return False 

	def place(self, grid, bat, pos, dir):
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
	mat = np.zeros(10, 10, np.int32)
	return