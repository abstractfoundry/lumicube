# Show ripples across the cube's LEDs
import random
import time
import math

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
                            if brightness > 0.05: # Don't show low brightness
                                leds[(x,y,z)] = hsv_colour(hue, sat, brightness)
        
    def finished(self):
        if (self.radius > 16):
            return True
        return False

display.set_all(black)
ripples = []
count = 0

while True:
    
    # Every 30 iterations create a new ripple
    if count % 30 == 0:
        # Pick a random 3d coordinate to start from
        (x, y, z) = [random.randint(0,7) for i in range(0,3)]
        # make it start on one of the faces
        panel = random.randint(0,3)
        if panel == 0:
            z = 8
        elif panel == 1:
            x = 8
        else:
            y = 8
        hsv = (random.random(), 1, 1)
        ripples.append(Ripple(x, y, z, hsv))
    
    # Initialise leds to black
    leds = {}
    for x in range(0,9):
        for y in range(0,9):
            for z in range(0,9):
                if x == 8 or y == 8 or z == 8:
                    leds[(x,y,z)] = 0;
    
    # Set leds for ripples
    for r in ripples:
        r.draw(leds)
    
    # Remove any ripples that have finished
    to_remove = []
    for r in ripples:
        if r.finished():
            to_remove.append(r)
    for r in to_remove:
        ripples.remove(r)
    
    display.set_3d(leds)
    time.sleep(1/20)
    count += 1
