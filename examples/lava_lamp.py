# Use simplex noise to generate a lava lamp like effect

# Simplex noise is way of generating random numbers across a 2D, 3D or 4D space
# whether each point is similar to its neighbour. So you get a randomised landscape with peaks and troughs
from opensimplex import OpenSimplex
import time

noise = OpenSimplex()
scale = 0.10 # How spread out are the features
speed = 0.05 # How fast things change
t = 0
while True:
    colours = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if x == 8 or y == 8 or z == 0:
                    # Noise returns a number between -1 and 1
                    hue = noise.noise4d(x * scale, y * scale, z * scale, t * speed) / 2 + 0.65
                    colours[(x,y,z)] = hsv_colour(hue, 1, 1)
    display.set_3d(colours)
    time.sleep(1/20)
    t += 1
