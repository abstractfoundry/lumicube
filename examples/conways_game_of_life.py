# Run Conway's Game of Life (https://en.wikipedia.org/wiki/Conway's_Game_of_Life).

import random
max_turns = 50
starting_live_ratio = 0.4
colour = random_colour()
num_turns = 0
alive_cells = []
for x in range(0,16):
    for y in range(0,16):
        if x < 8 or y < 8:
            if random.random() < starting_live_ratio:
                alive_cells.append((x,y))

def num_alive_neighbours(x, y):
    num_neighbours = 0
    for x2 in [x-1, x, x+1]:
        for y2 in [y-1, y, y+1]:
            if (x2, y2) != (x, y):
                neighbour = (x2, y2)
                # Account for 3D nature of panels
                if x2 == 8 and y2 >= 8:
                    neighbour = (y2, 7)
                elif y2 == 8 and x2 >= 8:
                    neighbour = (7, x2)
                if neighbour in alive_cells:
                    num_neighbours += 1
    return num_neighbours

while (num_turns < max_turns):
    next_cells = []
    leds = {}
    for x in range(0,16):
        for y in range(0,16):
            if x < 8 or y < 8:
                alive = (x, y) in alive_cells
                neighbours = num_alive_neighbours(x, y)
                # Remains alive
                if alive and (neighbours == 2
                        or neighbours == 3):
                    next_cells.append((x, y))
                    leds[x, y] = colour
                # Becomes alive
                elif not alive and neighbours == 3:
                    next_cells.append((x, y))
                    leds[x, y] = colour
                # Else dead
                else:
                    leds[x, y] = black
    alive_cells = next_cells
    display.set_leds(leds)
    time.sleep(0.3)
    num_turns += 1
