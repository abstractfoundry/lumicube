# Animate ripples across the cube's LEDs, which respond
# to tapping the cube (or accelerating it in some way).
# Note: Requires the advanced kit IMU add-on.

import threading

class Ripple:
    def __init__(self, start_x, start_y, start_z, hsv, velocity=10, wavefront_size=1.3):
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.hsv = hsv
        self.velocity = velocity
        self.wavefront_size = wavefront_size
        self.start_time = time.time()
        self.radius = 0

    def draw(self, leds):
        self.radius = self.velocity * (time.time() - self.start_time)
        for x in range(0,9):
            for y in range(0,9):
                for z in range(0,9):
                    if x == 8 or y == 8 or z == 8:
                        # Calculate how far this pixel is from the ripple line
                        distance = (abs(self.start_x - x) ** 2 + abs(self.start_y - y) ** 2 + abs(self.start_z - z) ** 2) ** (1/2)
                        dist_diff = abs(self.radius - distance)
                        if (dist_diff < self.wavefront_size):
                            # Set the brightness based on how close the pixel is to the ripple line
                            pos_brightness = math.cos(math.pi*dist_diff/(2*self.wavefront_size))
                            hue, sat, value = self.hsv
                            brightness = value*pos_brightness
                            if brightness > 0.05: # Set any low brightness LEDs black
                                leds[(x,y,z)] = hsv_colour(hue, sat, brightness)

    def finished(self):
        if (self.radius > 16):
            return True
        return False

# Check the acceleration in a separate thread to ensure we sample it at regular intervals
acc_direction = None
wait_count = 0
def worker():
    global acc_direction, wait_count
    avg_acc_x, avg_acc_y, avg_acc_z = 0, 0, 0
    while True:
        acc_x, acc_y, acc_z = (abs(imu.acceleration_x), abs(imu.acceleration_y), abs(imu.acceleration_z))
        avg_acc_x = avg_acc_x * 0.95 + acc_x * 0.05
        avg_acc_y = avg_acc_y * 0.95 + acc_y * 0.05
        avg_acc_z = avg_acc_z * 0.95 + acc_z * 0.05
        acc_x -= avg_acc_x
        acc_y -= avg_acc_y
        acc_z -= avg_acc_z
        max_acc = max(acc_x, acc_y, acc_z)
        if wait_count > 0:
            wait_count -= 1
        if max_acc > 0.15 and wait_count == 0:
            wait_count = 5
            if max_acc == acc_x:
                acc_direction = "x"
            elif max_acc == acc_y:
                acc_direction = "y"
            else:
                acc_direction = "z"
        time.sleep(0.02)
threading.Thread(target=worker, daemon=True).start()

display.set_all(black)
ripples = []

while True:
    # If an acceleration is detected create new ripple
    if acc_direction != None:
        # Make it start in the middle of the accelerated face
        if acc_direction == "x":
            x, y, z = 8, 4, 4
        elif acc_direction == "y":
            x, y, z = 4, 8, 4
        else:
            x, y, z = 4, 4, 0
        hsv = (random.random(), 1, 1)
        ripples.append(Ripple(x, y, z, hsv))
        # Reset the acceleration direction
        acc_direction = None

    # Initialise the LEDs to black
    leds = {}
    for x in range(0,9):
        for y in range(0,9):
            for z in range(0,9):
                if x == 8 or y == 8 or z == 8:
                    leds[(x,y,z)] = 0;

    # Draw all the ripples
    for r in ripples:
        r.draw(leds)

    # Remove any ripples that have finished
    to_remove = []
    for r in ripples:
        if r.finished():
            to_remove.append(r)
    for r in to_remove:
        ripples.remove(r)

    display.set_3d(leds, True)
    time.sleep(1/20)
