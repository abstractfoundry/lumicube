# Run Conway's Game of Life (https://en.wikipedia.org/wiki/Conway's_Game_of_Life)
# based on the AbstractFoundry code
# modified by Kirk Carlson
#   phased transitions between generations
#   allow generations to proceed to annihilation, stability or oscillation
#      while emphasizing the end


#### IMPORTS ####
import random

#### FUNCTIONS ####

# determine the number of alive neighbors
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


# determine if two lists are equivalent
def is_list_equal( list1, list2):
    if len( list1) != len( list2):
        return False
    for item in list1:
        if item not in list2:
            return False
    return True



#### CONFIGURATION CONSTANTS ####
starting_live_ratio = 0.4
guard_hue = 0.1 # portion of full circle
allowed_loops = 3
maximum_generations = 500
base_saturation = 1
base_luminance = 0.5


#### CONSTANTS ####
num_transitions = 5 # between state
num_phases = 2 * num_transitions
dead = 0
alive = num_transitions
dying = alive + 1
spark = dead + 1

#### MAIN LOOP ####
# VARIABLES
base_hue = 0
num_generations = 0
num_cells_start = 0
num_cells_left = 0
loop_length = 0
past_loop_length = 0
loop_count = 0
while True:
    # loop initialization
    if loop_length > 0:
        print ("hue: %4.2f start cells %2s, generations: %3s, cells at end: %2s, loop length: %2s" % ( base_hue, num_cells_start, num_generations, num_cells_left, loop_length) )
    base_hue = (base_hue + guard_hue + ( 1 - 2 * guard_hue) * random.random() ) % 1
    phaseColors = [ hsv_colour( base_hue, base_saturation,       0   * base_luminance), # dead
                    hsv_colour( base_hue, base_saturation,       0.2 * base_luminance), # spark
                    hsv_colour( base_hue, base_saturation,       0.4 * base_luminance),
                    hsv_colour( base_hue, base_saturation,       0.6 * base_luminance),
                    hsv_colour( base_hue, base_saturation,       0.8 * base_luminance),

                    hsv_colour( base_hue, base_saturation,       1   * base_luminance), # alive
                    hsv_colour( base_hue, base_saturation,       0.8 * base_luminance), # dying
                    hsv_colour( base_hue, base_saturation,       0.6 * base_luminance),
                    hsv_colour( base_hue, base_saturation,       0.4 * base_luminance),
                    hsv_colour( base_hue, base_saturation,       0.2 * base_luminance)
                  ]

    # seed the starting cells and build current_phases list of lists
    alive_cells = []
    current_phases = []
    for x in range( 16):
        column = []
        for y in range( 16):
            if (x < 8 or y < 8) and random.random() < starting_live_ratio:
                alive_cells.append( (x,y))
                column.append( spark)
            else:
                column.append( dead)
        current_phases.append( column)
    num_cells_start = len( alive_cells)

    num_generations = 0
    past_alives = []
    is_looping = False
    loop_count = 0
    past_loop_length = 0
    fail_safe_count = maximum_generations
    while not is_looping:

        # transition from current phase to final phase of current state
        leds = {}
        for t in range ( num_transitions):
            for x in range( 16):
                for y in range( 16):
                    if x < 8 or y < 8:
                        phase = current_phases[ x][ y]
                        leds[ x,y] = phaseColors [ phase]
                        if phase != dead and phase != alive:
                            current_phases[ x][ y] = (phase + 1) % num_phases
            display.set_leds( leds)
            time.sleep( 0.2)

        # determine if pattern is looping (too much)
        for count, past_alive_cells in enumerate( past_alives):
            if is_list_equal( alive_cells, past_alive_cells): # seen this before?
                loop_length = len( past_alives) - count
                if past_loop_length == 0:
                    past_loop_length = loop_length
                    loop_count = 1
                elif loop_length == past_loop_length:
                    loop_count += 1
                    if loop_count >= allowed_loops:
                        is_looping = True # now we've seen enough
        if len( past_alives) == 0 or past_loop_length == 0: # first pass or no loop detected
            past_alives.append( alive_cells)
            num_generations += 1

        # determine the state and phase for the next generation
        next_cells = []
        for x in range( 16):
            for y in range( 16):
                if x < 8 or y < 8:
                    is_alive = (x, y) in alive_cells
                    neighbours = num_alive_neighbours(x, y)

                    if is_alive:
                        if ( neighbours == 2 or neighbours == 3):
                            next_cells.append( ( x, y))
                            phase = alive
                        else:
                            phase = dying
                    elif neighbours == 3:
                        phase = spark
                        next_cells.append( ( x,y))
                    else: # dead
                        phase = dead
                    current_phases[ x][y] = phase

        num_cells_left = len( alive_cells)
        alive_cells = next_cells

        # stop VERY long non-repeating patterns
        fail_safe_count -= 1
        if fail_safe_count <= 0:
            print ("Fail safe triggered")
            is_looping = True
