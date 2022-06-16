# Pick up the cube and rotate it - this project makes it look like there is water inside.
# Note: Requires the advanced kit IMU add-on.

def dot_product(vector1, vector2):
    (x1,y1,z1) = vector1
    (x2,y2,z2) = vector2
    return (x1 * x2) + (y1 * y2) + (z1 * z2)

def led_below_water_level(x, y, z, gravity):
    mid_point_height = dot_product((4.5, 4.5, 4.5), gravity)
    led_bottom = (x, y, z)
    led_top = (x+1, y+1, z+1)
    max_height = max(dot_product(led_bottom, gravity), \
        dot_product(led_top, gravity))
    return (max_height < mid_point_height)

while True:
    gravity = (imu.gravity_x, imu.gravity_y, imu.gravity_z)
    leds = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if x == 8 or y == 8 or z == 8:
                    if led_below_water_level(x,y,z, gravity):
                        leds[x, y, z] = cyan
                    else:
                        leds[x, y, z] = black
    time.sleep(0.05)
    display.set_3d(leds)
