# Blow at the back of the cube to make the windmill animation turn
# It turns when it detects a rise in the humidity

import threading

humidity = 100

def worker():
    global humidity
    while True:
        humidity = env_sensor.humidity
        time.sleep(0.05)

threading.Thread(target=worker, daemon=True).start()

def windmill_shader(x, y, blade_angle):
    theta = 360 * (0.5 + math.atan2(y, x) / (2 * math.pi))
    modulo = (3 * theta) % 360
    difference = abs(modulo - blade_angle)
    return hsv_colour(0, 0, 500 / difference ** 2 if difference > 0 else 1)

decay = 0.07
sample_period = 0.025
threshold = 0.15
previous_sample = 100
next_sample_time = time.monotonic() + sample_period
accumulator = 0
blade_angle = 0
rotational_velocity = 0
max_velocity = 70
while True:
    now = time.monotonic()
    if time.monotonic() > next_sample_time:
        sample = humidity
        if sample > previous_sample + threshold:
            accumulator = 3
        previous_sample = sample
        next_sample_time = now + sample_period
    rotational_velocity = max_velocity * min(accumulator, 1)
    blade_angle = (blade_angle + rotational_velocity) % 360
    canvas = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if x == 8 or y == 8 or z == 8:
                    projected_x = (z + x - 8)
                    projected_y = (z + 2 * y - x - 8) / (3 ** 0.5)
                    canvas[(x,y,z)] = windmill_shader(projected_x, projected_y, blade_angle)
    display.set_3d(canvas, True)
    accumulator *= (1 - decay)
    time.sleep(1 / 25)