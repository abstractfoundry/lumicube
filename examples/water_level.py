# Pick up the cube and rotate it. This apps makes it look like there is water inside

def dot_product(vector1, vector2):
    (x1,y1,z1) = vector1
    (x2,y2,z2) = vector2
    return (x1 * x2) + (y1 * y2) + (z1 * z2)

while True:
    gravity = (imu.gravity_x, imu.gravity_y, imu.gravity_z)
    water_height = dot_product((4.5, 4.5, 4.5), gravity)
    leds = {}
    # Loop through each pixel in 3D space and work out whether it is below the water level or not
    for x in range(0,9):
        for y in range(0,9):
            for z in range(0,9):
                if x == 8 or y == 8 or z == 8:
                    bottom = (x, y, z)
                    top = (x+1, y+1, z+1)
                    max_height = max(dot_product(bottom, gravity), dot_product(top, gravity))
                    leds[(x, y, z)] = cyan if (max_height < water_height) else black
    display.set_3d(leds)