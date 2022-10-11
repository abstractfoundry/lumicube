# Every minute display the time - then run Conway's game of life on the digits

import random
import datetime


tall_font = [
	0b1011111111, 0b1111011111, 0b1011111111,
	0b1100111011, 0b0100000000, 0b1011100111,
	0b1000111011, 0b0100000000, 0b1011100111,
	0b1011111011, 0b0111111011, 0b1011111111,
	0b1010001010, 0b0100000000, 0b1001111111,
	0b1010001010, 0b0100000000, 0b1001111111,
	0b1010001010, 0b0100000000, 0b1001111111,
	0b1111011011, 0b1111011011, 0b1111111111
]

def draw_number(leds: dict, number: int, x_offset: int, y_offset: int, color: int) -> None:
	mask = pow(2, 9 - number)
	for y in range(8):
		for x in range(3):
			tf_index = (21 - (y * 3)) + (x % 3)
			tf_value = tall_font[tf_index]
			bit_on = bool(mask & tf_value)
			leds[x + x_offset, y + y_offset] = color if bit_on else 0


def draw_double_digit_number(leds: dict, number: int, x_offset: int, y_offset: int, color: int) -> None:
	draw_number(leds, number // 10, x_offset, y_offset, color)
	draw_number(leds, number % 10, x_offset + 4, y_offset, color)


while True:
    max_turns = 50
    colour = random_colour()
    num_turns = 0
    
    # Set the digits
    time_now = datetime.datetime.now()
    display.set_all(black)
    leds = {}
    draw_double_digit_number(leds, time_now.hour, 1,0, colour)
    display.set_leds(leds)
    leds2 = {}
    draw_double_digit_number(leds2, time_now.minute, 9,0, colour)
    display.set_leds(leds2)
    time.sleep(5)
    
    alive_cells = []
    for pos in leds.keys():
        alive_cells.append(pos)
    for pos in leds2.keys():
        alive_cells.append(pos)
    
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
    
    # Run Game of Life
    
    seconds = 0
    while (seconds < 60.0):
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
        seconds += 0.3
        num_turns += 1
