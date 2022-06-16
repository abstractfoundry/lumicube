# Generate a lava lamp effect using OpenSimplex noise.

def lava_colour(x, y, z, t):
    scale = 0.10
    speed = 0.05
    hue = noise_4d(scale * x, scale * y, scale * z, speed * t)
    return hsv_colour(hue, 1, 1)

def paint_cube(t):
    colours = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if x == 8 or y == 8 or z == 8:
                    colour = lava_colour(x, y, z, t)
                    colours[x,y,z] = colour
    display.set_3d(colours)

t = 0
while True:
    paint_cube(t)
    time.sleep(1/30)
    t += 1
