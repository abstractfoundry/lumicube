# Run Conways Game of Life with a randomised start
import random
import time

def update_leds(cells, colour):
	leds = {}
	for x in range(0,16):
		for y in range(0,16):
			if x < 8 or y < 8:
				leds[x,y] = colour if (x,y) in cells else black
	display.set_leds(leds)

def random_colour():
    return hsv_colour(random.uniform(-1.0,1.0),1,1)    
	
def random_setup(starting_live_ratio):
	cells = []
	for x in range(0,16):
		for y in range(0,16):
			if x < 8 or y < 8:
				if random.random() < starting_live_ratio:
					cells.append((x,y))
	return cells

def adjacent_positions(x, y, include_diagonal=False):
	positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
	if include_diagonal:
		positions = positions + [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
	mapped_positions = []
	for (x,y) in positions:
		if (x < 16 and x >= 0) and (y < 16 and y >= 0):
			# Account for 3D nature of panels
			if x > 7 and y > 7:
				if x > 7 and y == 8:
					mapped_positions.append((7, x))
				elif x == 8 and y > 7:
					mapped_positions.append((y, 7))
			# Make sure x and y are valid positions
			else:
				mapped_positions.append((x,y))
	return mapped_positions

def num_neighbours(x, y, cells):
	return len(set(cells).intersection(adjacent_positions(x, y, include_diagonal=True)))

def run_game_of_life(cells, colour, period, max_iterations):
	update_leds(cells, colour)
	iterations = 0
	while 1:
		next_cells = cells.copy()
		for x in range(0,16):
			for y in range(0,16):
				if x < 8 or y < 8:
					neighbours = num_neighbours(x, y, cells)
					pos = (x,y)
					# If alive
					if pos in cells:
						if neighbours < 2 or neighbours > 3:
							# Dies
							next_cells.remove(pos)
					else:
						if neighbours == 3:
							# New life
							next_cells.append(pos)
		update_leds(next_cells, colour)
		# End if nothing is changing or after enough iterations
		if set(next_cells) == set(cells) or iterations > max_iterations:
			break
		cells = next_cells
		time.sleep(period)
		iterations+=1


while 1:
	# cells = [(2,4), (3,4), (4,4), (5,4), (6,4),
	# 		(2+6,4), (3+6,4), (4+6,4), (5+6,4), (6+6,4),
	# 		(2,10), (3,10), (4,10), (5,10), (6,10), ]
	cells = random_setup(0.4)
	run_game_of_life(cells, random_colour(), 0.3, 50)
	# Sleep before next simulation
	time.sleep(3)
